import { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Бизнес-модель · UY-CLICK',
  description: 'Как UY-CLICK зарабатывает и развивает платформу аренды жилья в Узбекистане.',
};

const streams = [
  { title: 'Premium-объявления', icon: '★', color: 'amber', desc: 'Платное продвижение в верхней части выдачи. Арендодатели с активной недвижимостью охотно платят за приоритет.' },
  { title: 'Pro-подписка', icon: '⚡', color: 'teal', desc: 'Ежемесячный план ($12/мес) или годовой ($9.6/мес) для активных арендодателей: расширенная аналитика и приоритет в поиске.' },
  { title: 'Разовые листинги', icon: '📌', color: 'blue', desc: 'Заплати один раз — объявление в топе на 7 или 30 дней. Удобно для тех, кто не хочет подписку.' },
  { title: 'Агентский тариф', icon: '🏢', color: 'purple', desc: 'Корпоративный доступ для агентств с несколькими аккаунтами и единым биллингом.' },
  { title: 'Верификация объектов', icon: '✓', color: 'green', desc: 'Значок «Проверено» на объявлении после физической проверки объекта или верификации документов.' },
  { title: 'Партнёрства', icon: '🤝', color: 'rose', desc: 'Интеграции с управляющими компаниями, ЖКХ-сервисами и переездами — revenue share с партнёров.' },
];

const colorMap: Record<string, string> = {
  amber: 'bg-amber-50 border-amber-200 text-amber-700',
  teal: 'bg-teal-50 border-teal-200 text-teal-700',
  blue: 'bg-blue-50 border-blue-200 text-blue-700',
  purple: 'bg-purple-50 border-purple-200 text-purple-700',
  green: 'bg-green-50 border-green-200 text-green-700',
  rose: 'bg-rose-50 border-rose-200 text-rose-700',
};

export default function MonetizationPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-extrabold text-gray-900">Как устроена экономика UY-CLICK</h1>
        <p className="text-gray-500 max-w-2xl mx-auto">Платформа бесплатна для базового использования. Монетизация строится на премиальных инструментах для тех, кто сдаёт жильё профессионально.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {streams.map((s) => (
          <div key={s.title} className={`rounded-2xl border p-5 space-y-2 ${colorMap[s.color]}`}>
            <div className="text-2xl">{s.icon}</div>
            <h3 className="font-bold text-gray-900">{s.title}</h3>
            <p className="text-sm text-gray-600 leading-relaxed">{s.desc}</p>
          </div>
        ))}
      </div>

      <div className="bg-gray-50 rounded-2xl border border-gray-200 p-6 space-y-3">
        <h2 className="text-lg font-bold text-gray-900">Принципы</h2>
        <ul className="space-y-2 text-sm text-gray-700">
          <li className="flex items-start gap-2"><span className="text-teal-500 mt-0.5">→</span><span><strong>Ноль комиссий с арендатора.</strong> Тот, кто ищет жильё, не платит ничего.</span></li>
          <li className="flex items-start gap-2"><span className="text-teal-500 mt-0.5">→</span><span><strong>Платит тот, кто зарабатывает.</strong> Арендодатель платит только за инструменты, которые ускоряют сдачу.</span></li>
          <li className="flex items-start gap-2"><span className="text-teal-500 mt-0.5">→</span><span><strong>Прозрачность.</strong> Платные объявления помечены — пользователь всегда знает, что видит рекламу.</span></li>
        </ul>
      </div>

      <div className="text-center">
        <Link href="/profile" className="inline-flex items-center gap-2 px-5 py-2.5 bg-teal-600 text-white font-semibold rounded-xl hover:bg-teal-700 transition-colors">
          Посмотреть тарифы
        </Link>
      </div>
    </div>
  );
}
