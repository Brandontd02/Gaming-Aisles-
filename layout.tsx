import type React from "react"
import { ThemeProvider } from "@/components/theme-provider"
import "./globals.css"
import type { Metadata } from "next"
import { VT323, Permanent_Marker } from "next/font/google"

// Load fonts using next/font
const vt323 = VT323({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-vt323",
  display: "swap",
})

const permanentMarker = Permanent_Marker({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-permanent-marker",
  display: "swap",
})

export const metadata: Metadata = {
  title: "Forgotten Gems - Nostalgic Game Store",
  description: "Discover hidden gems from the golden age of gaming",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning className={`${vt323.variable} ${permanentMarker.variable}`}>
      <body>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem={false} themes={["light", "dark", "crt"]}>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
