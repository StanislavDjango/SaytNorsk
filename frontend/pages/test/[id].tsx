import { useRouter } from 'next/router'
import { useState, useRef, useEffect } from 'react'
import Header from '@/components/Header'
import FillInTheBlank from '@/components/FillInTheBlank'
import Results from '@/components/Results'
import ProgressBar from '@/components/ProgressBar'
import { apiService, Test } from '@/lib/api'
import { useTranslations } from '@/lib/i18n'

export default function TestPage() {
  const router = useRouter()
  const { id } = router.query
  const [test, setTest] = useState<Test | null>(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [studentName, setStudentName] = useState('')
  const [testStarted, setTestStarted] = useState(false)
  const [answers, setAnswers] = useState<any[]>([])
  const [results, setResults] = useState<any | null>(null)
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState('')
  const studentNameRef = useRef<HTMLInputElement>(null)
  const { t } = useTranslations()

  useEffect(() => {
    if (!id) return

    const fetchTest = async () => {
      try {
        setLoading(true)
        setLoadError('')
        const data = await apiService.getTest(Number(id))
        setTest(data)
      } catch (err) {
        setLoadError(t('testLoadError'))
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchTest()
  }, [id, t])

  if (loading) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-2xl mx-auto text-center">
            <p className="text-xl text-gray-600">{t('loading')}</p>
          </div>
        </main>
      </>
    )
  }

  if (loadError || !test) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8 text-center">
            <p className="text-xl text-gray-600">{loadError || t('testNotFound')}</p>
          </div>
        </main>
      </>
    )
  }

  if (!test.questions || test.questions.length === 0) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8 text-center">
            <p className="text-xl text-gray-600">{t('noQuestions')}</p>
          </div>
        </main>
      </>
    )
  }

  const handleStartTest = () => {
    if (!studentNameRef.current?.value.trim()) {
      alert(t('enterNamePrompt'))
      return
    }
    setStudentName(studentNameRef.current.value)
    setTestStarted(true)
  }

  const handleAnswer = (answer: string) => {
    setAnswers([...answers, { question_id: test.questions[currentQuestionIndex].id, answer }])
  }

  const handleNextQuestion = () => {
    if (currentQuestionIndex < test.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    } else {
      submitTest()
    }
  }

  const submitTest = async () => {
    try {
      const result = await apiService.submitTest(test.id, studentName, answers)
      setResults(result)
    } catch (error) {
      console.error('Error submitting test:', error)
      alert(t('submitError'))
    }
  }

  const handleTryAgain = () => {
    setCurrentQuestionIndex(0)
    setAnswers([])
    setResults(null)
    setTestStarted(false)
    setStudentName('')
  }

  const handleBack = () => {
    router.back()
  }

  // Name Entry Screen
  if (!testStarted && !results) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg p-8">
              <h1 className="text-4xl font-bold text-gray-800 mb-4">{test.title}</h1>
              <p className="text-gray-600 mb-8">{test.description}</p>

              <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-8">
                <p className="text-sm text-blue-700">
                  {t('containsQuestions', { count: test.questions.length })}
                </p>
              </div>

              <div className="mb-6">
                <label className="block text-lg font-semibold text-gray-700 mb-2">
                  {t('nameLabel')}
                </label>
                <input
                  ref={studentNameRef}
                  type="text"
                  placeholder={t('namePlaceholder')}
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-600 text-lg"
                  onKeyPress={(e) => e.key === 'Enter' && handleStartTest()}
                />
              </div>

              <button
                onClick={handleStartTest}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-lg transition"
              >
                {t('startTest')}
              </button>
            </div>
          </div>
        </main>
      </>
    )
  }

  // Test In Progress
  if (testStarted && !results) {
    const currentQuestion = test.questions[currentQuestionIndex]

    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <div className="max-w-2xl mx-auto">
            <ProgressBar current={currentQuestionIndex + 1} total={test.questions.length} />

            <FillInTheBlank
              question={currentQuestion}
              onAnswer={handleAnswer}
              onNext={handleNextQuestion}
              isLast={currentQuestionIndex === test.questions.length - 1}
            />
          </div>
        </main>
      </>
    )
  }

  // Results Screen
  if (results) {
    return (
      <>
        <Header />
        <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
          <Results
            score={results.correct_answers}
            total={results.total_questions}
            grade={results.score_letter}
            answers={results.answers}
            onTryAgain={handleTryAgain}
            onBack={handleBack}
          />
        </main>
      </>
    )
  }

  return null
}
