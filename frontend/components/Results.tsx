import { motion } from 'framer-motion'
import { useTranslations } from '@/lib/i18n'

interface ResultsProps {
  score: number
  total: number
  grade: string
  answers: any[]
  showCorrectAnswers?: boolean
  onTryAgain: () => void
  onBack: () => void
}

export default function Results({
  score,
  total,
  grade,
  answers,
  showCorrectAnswers = true,
  onTryAgain,
  onBack,
}: ResultsProps) {
  const { t } = useTranslations()
  const percentage = Math.round((score / total) * 100)
  const summary = t('scoreSummary', { score, total, percentage })

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="w-full max-w-2xl mx-auto p-6"
    >
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-4xl font-bold text-center mb-8">{t('resultsTitle')}</h1>

        {/* Score Card */}
        <div
          className={`text-center mb-8 p-6 rounded-lg ${
            percentage >= 80 ? 'bg-green-100' : percentage >= 60 ? 'bg-yellow-100' : 'bg-red-100'
          }`}
        >
          <div className="text-6xl font-bold mb-2">{percentage}%</div>
          <div className="text-2xl font-semibold mb-2">{summary}</div>
          <div className="text-xl">{t('gradeLabel', { grade })}</div>
        </div>

        {/* Error Breakdown */}
        {showCorrectAnswers && (
          <div className="mb-8">
            <h2 className="text-2xl font-semibold mb-4">{t('answerReview')}</h2>
            <div className="space-y-4">
              {answers.map((answer: any, index: number) => (
                <div
                  key={index}
                  className={`p-4 rounded-lg border-l-4 ${
                    answer.is_correct
                      ? 'border-green-500 bg-green-50'
                      : 'border-red-500 bg-red-50'
                  }`}
                >
                  <div className="font-semibold text-gray-800">
                    {answer.is_correct ? t('correct') : t('incorrect')}
                  </div>
                  <div className="text-sm text-gray-600">
                    {t('yourAnswer')} <span className="font-mono">{answer.student_answer}</span>
                  </div>
                  {!answer.is_correct && (
                    <div className="text-sm text-green-700">
                      {t('correctAnswer')}{' '}
                      <span className="font-mono">{answer.correct_answer}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-4 justify-center">
          <button
            onClick={onTryAgain}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-lg transition"
          >
            {t('tryAgain')}
          </button>
          <button
            onClick={onBack}
            className="px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-semibold rounded-lg transition"
          >
            {t('back')}
          </button>
        </div>
      </div>
    </motion.div>
  )
}
