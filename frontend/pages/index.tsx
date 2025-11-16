import { useEffect, useState } from 'react'
import Link from 'next/link'
import Header from '@/components/Header'
import { apiService, Lesson } from '@/lib/api'
import { useTranslations } from '@/lib/i18n'

export default function Home() {
  const [lessons, setLessons] = useState<Lesson[]>([])
  const [loading, setLoading] = useState(true)
  const { t, formatTestCount } = useTranslations()

  useEffect(() => {
    fetchLessons()
  }, [])

  const fetchLessons = async () => {
    try {
      const data = await apiService.getLessons()
      setLessons(data)
    } catch (error) {
      console.error('Error fetching lessons:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-7xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-800 mb-4">{t('heroTitle')}</h1>
            <p className="text-xl text-gray-600">{t('heroSubtitle')}</p>
          </div>

          {/* Lessons Grid */}
          {loading ? (
            <div className="text-center text-xl text-gray-600">{t('loading')}</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {lessons.map((lesson) => (
                <Link
                  key={lesson.id}
                  href={`/lesson/${lesson.id}`}
                  className="transform transition hover:scale-105"
                >
                  <div className="bg-white rounded-lg shadow-lg p-6 cursor-pointer h-full">
                    <div className="flex items-start justify-between mb-4">
                      <h2 className="text-2xl font-bold text-gray-800 flex-1">{lesson.title}</h2>
                      <span className="inline-block bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-semibold">
                        {lesson.level}
                      </span>
                    </div>
                    <p className="text-gray-600 mb-4 line-clamp-2">{lesson.description}</p>
                    <div className="text-sm text-gray-500">
                      {formatTestCount(lesson.tests.length)}
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}

          {!loading && lessons.length === 0 && (
            <div className="text-center py-12">
              <p className="text-xl text-gray-600">{t('noLessons')}</p>
            </div>
          )}
        </div>
      </main>
    </>
  )
}
