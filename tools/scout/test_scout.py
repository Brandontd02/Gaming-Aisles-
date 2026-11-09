"""Offline regression tests for Scout v2. No tokens, network or Airtable writes."""
import unittest

from scout import (PageDescription, canonical, feed_games, itch_game_url,
                   name_key, rule_rank, title_only)


def game(title, desc, *, free=False, feeds=None):
    return {"title": title, "desc": desc, "free": free, "feeds": set(feeds or [])}


class ScoutTests(unittest.TestCase):
    def test_generic_simulation_is_not_cipher(self):
        self.assertIsNone(rule_rank(game("Simulation Game", "A new simulation of city life")))

    def test_music_alone_is_not_flow(self):
        self.assertIsNone(rule_rank(game("Neon Plaza", "A platformer with a nice soundtrack")))

    def test_mechanical_rhythm_qualifies(self):
        result = rule_rank(game("Beatbreak",
            "Rhythm-based combat and timing-based moves create a mastery loop."))
        self.assertEqual(result["pillar"], "Rhythm & Flow")
        self.assertEqual(result["shelf"], "Flow State")

    def test_uncanny_atmosphere_is_dread(self):
        result = rule_rank(game("Lost Corridor",
            "Unsettling liminal environments and analog horror in a dreamlike world.", free=True))
        self.assertEqual(result["pillar"], "Atmosphere & Dread")
        self.assertEqual(result["shelf"], "Return Bin")

    def test_institutional_agency_is_cipher(self):
        result = rule_rank(game("The Inquiry",
            "Political intrigue, detective investigation and systemic oppression."))
        self.assertEqual(result["pillar"], "The Cipher")
        self.assertEqual(result["shelf"], "Unclear")

    def test_brackets_removed_from_feed_title(self):
        self.assertEqual(title_only("Arcade Kid [Free] [Rhythm] [Windows]"), "Arcade Kid")
        self.assertEqual(name_key("Arcade Kid [Free]"), name_key("arcade-kid"))

    def test_url_queries_are_ignored_for_dedup(self):
        self.assertEqual(canonical("https://x.itch.io/g/"),
                         canonical("https://x.itch.io/g?ref=feed"))

    def test_only_itch_game_subdomains_accepted(self):
        self.assertTrue(itch_game_url("https://foo.itch.io/test"))
        self.assertFalse(itch_game_url("https://itch.io/games"))
        self.assertFalse(itch_game_url("https://foo.itch.io.evil.invalid/test"))

    def test_rss_feed_parses(self):
        rss = b'<rss><channel><item><title>Odd Game [Free]</title><link>https://odd.itch.io/game</link><description>Surreal adventure</description></item></channel></rss>'
        records = list(feed_games(rss))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][0], "Odd Game")

    def test_page_description_isolated(self):
        parser = PageDescription()
        parser.feed('<meta name="description" content="fallback"><div class="formatted_description"><p>Uncanny</p><p>world</p></div><script>evil()</script>')
        self.assertIn("Uncanny", parser.excerpt())
        self.assertNotIn("evil", parser.excerpt())


if __name__ == "__main__":
    unittest.main()
