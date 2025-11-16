import Link from 'next/link'
import { useRouter } from 'next/router'
import { supportedLocales, useTranslations } from '@/lib/i18n'

export default function Header() {
  const router = useRouter()
  const { t, locale } = useTranslations()

  const changeLanguage = (nextLocale: string) => {
    router.push(router.pathname, router.asPath, { locale: nextLocale })
  }

  return (
    <header className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-blue-600">
          {t('siteName')}
        </Link>

        <nav className="flex items-center gap-6">
          <Link href="/" className="text-gray-700 hover:text-blue-600">
            {t('lessons')}
          </Link>

          <div className="flex gap-2" aria-label={t('language')}>
            {supportedLocales.map((lang) => (
              <button
                key={lang.code}
                type="button"
                onClick={() => changeLanguage(lang.code)}
                className={`px-3 py-1 rounded ${
                  locale === lang.code
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </nav>
      </div>
    </header>
  )
}
