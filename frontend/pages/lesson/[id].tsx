import { useEffect, useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'
import Header from '@/components/Header'
import { apiService, Lesson } from '@/lib/api'
import { useTranslations } from '@/lib/i18n'

export default function LessonPage() {
  const router = useRouter()
  const { id } = router.query
  const [lesson, setLesson] = useState<Lesson | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const { t, formatQuestionCount, formatTestType } = useTranslations()

  useEffect(() => {
    if (!id) return

    const loadLesson = async () => {
      try {
        setLoading(true)
        setError('')
        const data = await apiService.getLesson(Number(id))
        setLesson(data)
      } catch (err) {
        setError(t('lessonLoadError'))
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    loadLesson()
  }, [id, t])

  if (loading) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-4xl mx-auto text-center">
            <p className="text-xl text-gray-600">{t('loading')}</p>
          </div>
        </main>
      </>
    )
  }

  if (error || !lesson) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-4xl mx-auto">
            <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
              <p className="text-lg text-red-700">{error || t('lessonNotFound')}</p>
              <Link href="/" className="text-blue-600 hover:underline mt-4 inline-block">
                {t('backToLessons')}
              </Link>
            </div>
          </div>
        </main>
      </>
    )
  }

  return (
    <>
      <Header />
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
        <div className="max-w-4xl mx-auto">
          {/* Breadcrumb */}
          <Link href="/" className="text-blue-600 hover:text-blue-700 mb-6 inline-block">
            {t('backToLessons')}
          </Link>

          {/* Lesson Header */}
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-4">{lesson.title}</h1>
            <p className="text-lg text-gray-600 mb-4">{lesson.description}</p>
            <div className="inline-block bg-blue-100 text-blue-800 px-4 py-2 rounded-lg font-semibold">
              {t('levelLabel')}: {lesson.level}
            </div>
          </div>

          {/* Tests Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {lesson.tests.map((test) => (
              <div
                key={test.id}
                className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition"
              >
                <h2 className="text-2xl font-bold text-gray-800 mb-2">{test.title}</h2>
                <p className="text-gray-600 mb-4 line-clamp-2">{test.description}</p>
                <div className="text-sm text-gray-500 mb-4">
                  {formatQuestionCount(test.questions.length)} ({formatTestType(test.test_type)})
                </div>
                <Link
                  href={`/test/${test.id}`}
                  className="inline-block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition"
                >
                  {t('startTest')}
                </Link>
              </div>
            ))}
          </div>

          {lesson.tests.length === 0 && (
            <div className="bg-white rounded-lg shadow-lg p-8 text-center">
              <p className="text-xl text-gray-600">{t('noTests')}</p>
            </div>
          )}
        </div>
      </main>
    </>
  )
}
