"use client"
import React from 'react'
import { useState, useEffect } from 'react'
import { Button } from "./components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card"
import { ChartContainer, ChartTooltip, ChartTooltipContent } from "./components/ui/chart"
import { Bar, BarChart, XAxis, YAxis } from "recharts"

// This would be replaced with the actual URL of your FastAPI backend
const API_URL = 'http://localhost:8000'

interface GenreData {
  genre: string
  count: number
}

interface ClosestMatch {
  genre: string
  similarity: number
}

export default function Vibecheck() {
  const [genreData, setGenreData] = useState<GenreData[]>([])
  const [closestMatch, setClosestMatch] = useState<ClosestMatch | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: window.location.href,
          // You might want to store user preferences in Chrome storage
          // and retrieve them here
          user_preferences: ['techno', 'house', 'electronic'],
        }),
      })
      if (!response.ok) {
        throw new Error('Failed to fetch data')
      }
      const data = await response.json()
      setGenreData(data.genre_histogram)
      setClosestMatch(data.closest_match)
    } catch (err) {
      setError('Failed to analyze genres. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // You might want to auto-fetch data when the component mounts
    // fetchData()
  }, [])

  return (
    <Card className="w-96 fixed top-4 right-4 z-50 shadow-lg">
      <CardHeader>
        <CardTitle>Vibecheck</CardTitle>
        <CardDescription>Analyze genres for this event</CardDescription>
      </CardHeader>
      <CardContent>
        <Button onClick={fetchData} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Genres'}
        </Button>
        {error && <p className="text-red-500 mt-2">{error}</p>}
        {genreData.length > 0 && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold mb-2">Genre Distribution</h3>
            <ChartContainer
              config={{
                count: {
                  label: "Count",
                  color: "hsl(var(--chart-1))",
                },
              }}
              className="h-[200px]"
            >
              <BarChart data={genreData}>
                <XAxis dataKey="genre" />
                <YAxis />
                <ChartTooltip content={<ChartTooltipContent />} />
                <Bar dataKey="count" fill="var(--color-count)" />
              </BarChart>
            </ChartContainer>
          </div>
        )}
        {closestMatch && (
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Closest Match to Your Preferences</h3>
            <p>{closestMatch.genre} (Similarity: {(closestMatch.similarity * 100).toFixed(2)}%)</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}