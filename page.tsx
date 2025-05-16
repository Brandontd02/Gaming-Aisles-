"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"
import { ChevronLeft } from "lucide-react"

export default function SubmitGamePage() {
  const [formData, setFormData] = useState({
    gameName: "",
    platform: "",
    youtubeLink: "",
    whySpecial: "",
    email: "",
  })
  const [submitted, setSubmitted] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // In a real app, you would submit this data to your backend
    console.log("Form submitted:", formData)
    setSubmitted(true)
  }

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      <div className="container mx-auto px-4 py-12">
        <Link href="/" className="inline-flex items-center text-blue-400 hover:text-blue-300 mb-8">
          <ChevronLeft className="h-5 w-5 mr-1" />
          Back to Home
        </Link>

        <div className="max-w-3xl mx-auto">
          <div className="relative bg-blue-900/30 rounded-lg overflow-hidden border border-blue-800">
            {/* VHS effects */}
            <div className="absolute inset-0 opacity-20 mix-blend-overlay pointer-events-none bg-gradient-to-br from-blue-900/20 via-transparent to-purple-900/20"></div>
            <div className="absolute inset-0 opacity-10 pointer-events-none bg-gradient-to-b from-transparent via-blue-900/10 to-transparent"></div>

            <div className="bg-blue-800/50 p-4">
              <h1 className="text-2xl md:text-3xl font-bold text-white text-center">SUGGEST A HIDDEN GEM</h1>
            </div>

            <div className="p-6 md:p-8">
              {!submitted ? (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="flex items-center justify-between mb-8">
                    <div className="bg-yellow-400 text-slate-900 px-4 py-2 rounded-md font-bold transform -rotate-2">
                      MEMBERSHIP FORM
                    </div>
                    <div className="bg-blue-600 text-white px-4 py-2 rounded-md font-bold">GEM HUNTER</div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label htmlFor="gameName" className="block text-blue-300 font-medium">
                        Game Name
                      </label>
                      <input
                        type="text"
                        id="gameName"
                        name="gameName"
                        value={formData.gameName}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-2 bg-slate-800 border border-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      />
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="platform" className="block text-blue-300 font-medium">
                        Platform
                      </label>
                      <select
                        id="platform"
                        name="platform"
                        value={formData.platform}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-2 bg-slate-800 border border-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">Select Platform</option>
                        <option value="PC">PC</option>
                        <option value="Switch">Nintendo Switch</option>
                        <option value="PlayStation">PlayStation</option>
                        <option value="Xbox">Xbox</option>
                        <option value="Mobile">Mobile</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="youtubeLink" className="block text-blue-300 font-medium">
                      YouTube Video Recommendation (Optional)
                    </label>
                    <input
                      type="url"
                      id="youtubeLink"
                      name="youtubeLink"
                      value={formData.youtubeLink}
                      onChange={handleChange}
                      placeholder="https://youtube.com/watch?v=..."
                      className="w-full px-4 py-2 bg-slate-800 border border-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="whySpecial" className="block text-blue-300 font-medium">
                      Why is this game special?
                    </label>
                    <textarea
                      id="whySpecial"
                      name="whySpecial"
                      value={formData.whySpecial}
                      onChange={handleChange}
                      required
                      rows={4}
                      className="w-full px-4 py-2 bg-slate-800 border border-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    ></textarea>
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="email" className="block text-blue-300 font-medium">
                      Your Email (Optional)
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="For updates on your submission"
                      className="w-full px-4 py-2 bg-slate-800 border border-blue-700 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div className="pt-4">
                    <button
                      type="submit"
                      className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-md transition-colors glow-effect"
                    >
                      Submit to the Aisle
                    </button>
                  </div>
                </form>
              ) : (
                <div className="text-center py-12">
                  <div className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md font-bold mb-6">
                    GEM HUNTER BADGE EARNED!
                  </div>
                  <h2 className="text-2xl font-bold mb-4">Thanks for your submission!</h2>
                  <p className="text-slate-300 mb-8">
                    Our clerks will review your hidden gem recommendation and add it to our collection if it meets our
                    criteria.
                  </p>
                  <Link
                    href="/"
                    className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-md transition-colors"
                  >
                    Return to Home
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
