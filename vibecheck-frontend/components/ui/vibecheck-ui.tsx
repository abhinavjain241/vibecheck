"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Slider } from "@/components/ui/slider"
import { CalendarIcon, Clock, MapPin, Music } from "lucide-react"

const API_BASE_URL = 'http://0.0.0.0:8000';  // or 'http://localhost:8000' if 0.0.0.0 doesn't work

// Add these functions at the top of your component
const fetchEvents = async (startDate: string, endDate: string) => {
  const response = await fetch(`${API_BASE_URL}/callback?start_date=${startDate}&end_date=${endDate}`);
  if (!response.ok) {
    throw new Error('Failed to fetch events');
  }
  return response.json();
};

const createSpotifyPlaylist = async (eventId: string) => {
  const response = await fetch(`${API_BASE_URL}/create_playlist/${eventId}`, { method: 'POST' });
  if (!response.ok) {
    throw new Error('Failed to create playlist');
  }
  return response.json();
};

export default function Component() {
  const [events, setEvents] = useState([
    {
      id: "1",
      title: "Techno Night",
      image: "/placeholder.svg?height=100&width=200",
      date: "2023-06-15",
      startTime: "22:00",
      endTime: "04:00",
      venue: "Underground Club",
      genres: { "Techno": 80, "House": 20 },
    },
    {
      id: "2",
      title: "Jazz in the Park",
      image: "/placeholder.svg?height=100&width=200",
      date: "2023-06-18",
      startTime: "19:00",
      endTime: "23:00",
      venue: "Central Park",
      genres: { "Jazz": 90, "Blues": 10 },
    },
  ])

  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Add this effect to fetch events when the component mounts
  useEffect(() => {
    const fetchInitialEvents = async () => {
      setLoading(true);
      try {
        const today = new Date().toISOString().split('T')[0];
        const oneMonthLater = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        const fetchedEvents = await fetchEvents(today, oneMonthLater);
        setEvents(fetchedEvents);
      } catch (err) {
        setError('Failed to fetch events');
      } finally {
        setLoading(false);
      }
    };
    fetchInitialEvents();
  }, []);

  // Add this function to handle fetching events
  const handleGetEvents = async () => {
    setLoading(true);
    setError(null);
    try {
      const fetchedEvents = await fetchEvents(startDate, endDate);
      setEvents(fetchedEvents);
    } catch (err) {
      setError('Failed to fetch events');
    } finally {
      setLoading(false);
    }
  };

  // Add this function to handle creating a Spotify playlist
  const handleCreatePlaylist = async (eventId: string) => {
    try {
      await createSpotifyPlaylist(eventId);
      // You might want to show a success message here
    } catch (err) {
      setError('Failed to create playlist');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <div className="container mx-auto p-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2">vibecheck</h1>
          <Button variant="outline">Login with Spotify</Button>
        </header>
        <main>
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Find Events</h2>
            <div className="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4 mb-4">
              <div className="flex-1">
                <Label htmlFor="start-date" className="mb-2 block">Start Date</Label>
                <Input 
                  id="start-date" 
                  type="date" 
                  className="bg-gray-800 text-white" 
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                />
              </div>
              <div className="flex-1">
                <Label htmlFor="end-date" className="mb-2 block">End Date</Label>
                <Input 
                  id="end-date" 
                  type="date" 
                  className="bg-gray-800 text-white" 
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                />
              </div>
            </div>
            <Button onClick={handleGetEvents} disabled={loading}>
              {loading ? 'Loading...' : 'Get Events'}
            </Button>
          </section>
          <section className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">Your Top Genres</h2>
            <div className="space-y-4">
              {["Electronic", "Rock", "Hip-Hop", "Jazz"].map((genre) => (
                <div key={genre} className="flex items-center">
                  <span className="w-24">{genre}</span>
                  <Slider className="flex-1" defaultValue={[Math.random() * 100]} max={100} step={1} />
                </div>
              ))}
            </div>
          </section>
          <section>
            <h2 className="text-2xl font-semibold mb-4">Recommended Events</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.map((event) => (
                <Card key={event.id} className="bg-gray-800 text-gray-100">
                  <CardHeader>
                    <CardTitle>{event.title}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <img src={event.image} alt={event.title} className="w-full h-40 object-cover mb-4 rounded" />
                    <div className="space-y-2">
                      <div className="flex items-center">
                        <CalendarIcon className="mr-2 h-4 w-4" />
                        <span>{event.date}</span>
                      </div>
                      <div className="flex items-center">
                        <Clock className="mr-2 h-4 w-4" />
                        <span>{event.startTime} - {event.endTime}</span>
                      </div>
                      <div className="flex items-center">
                        <MapPin className="mr-2 h-4 w-4" />
                        <span>{event.venue}</span>
                      </div>
                      <div className="flex items-center">
                        <Music className="mr-2 h-4 w-4" />
                        <div className="flex-1">
                          {Object.entries(event.genres).map(([genre, percentage]) => (
                            <div key={genre} className="flex items-center">
                              <span className="w-16">{genre}</span>
                              <div className="flex-1 bg-gray-700 h-2 rounded">
                                <div
                                  className="bg-blue-500 h-2 rounded"
                                  style={{ width: `${percentage}%` }}
                                />
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                    {error && <p className="text-red-500 mt-2">{error}</p>}
                    <Button 
                      className="w-full mt-4" 
                      onClick={() => handleCreatePlaylist(event.id)}
                    >
                      Create Spotify Playlist
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}
