import Image from 'next/image'
import { useState } from 'react'
import { motion } from 'framer-motion'
import { useTranslations } from '@/lib/i18n'

interface FillInTheBlankProps {
  question: any
  onAnswer: (answer: string) => void
  onNext: () => void
  isLast: boolean
}

export default function FillInTheBlank({
  question,
  onAnswer,
  onNext,
  isLast,
}: FillInTheBlankProps) {
  const [answer, setAnswer] = useState('')
  const { t } = useTranslations()

  const handleSubmit = () => {
    if (answer.trim()) {
      onAnswer(answer)
      setAnswer('')
      onNext()
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      className="w-full max-w-2xl mx-auto p-6"
    >
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="mb-6">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            {question.text}
          </h2>

          {question.image && (
            <div className="mb-4">
              <Image
                src={question.image}
                alt={t('questionImageAlt')}
                width={400}
                height={250}
                className="rounded max-w-sm h-auto"
              />
            </div>
          )}

          {question.audio_file && (
            <audio controls className="w-full mb-4">
              <source src={question.audio_file} type="audio/mpeg" />
              Your browser does not support the audio element.
            </audio>
          )}
        </div>

        <div className="mb-6">
          <input
            type="text"
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
            placeholder={t('answerPlaceholder')}
            className="w-full px-4 py-3 border-2 border-blue-300 rounded-lg focus:outline-none focus:border-blue-600 text-lg"
            autoFocus
          />
        </div>

        <button
          onClick={handleSubmit}
          disabled={!answer.trim()}
          className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 rounded-lg transition"
        >
          {isLast ? t('submit') : t('next')}
        </button>
      </div>
    </motion.div>
  )
}
