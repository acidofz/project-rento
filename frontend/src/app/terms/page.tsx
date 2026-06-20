import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Правила площадки · UY-CLICK',
  description: 'Условия использования платформы UY-CLICK — аренда жилья без посредников.',
};

export default function TermsPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8 prose prose-gray">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Правила площадки</h1>

      <section className="space-y-4 text-sm text-gray-700 leading-relaxed">
        <div className="bg-teal-50 border border-teal-200 rounded-xl p-4">
          <p className="font-semibold text-teal-800">Добро пожаловать на UY-CLICK</p>
          <p className="text-teal-700 mt-1">Платформа соединяет арендаторов и арендодателей напрямую — без посредников и скрытых комиссий.</p>
        </div>

        <h2 className="text-lg font-bold text-gray-900 mt-6">1. Принятие условий</h2>
        <p>Используя UY-CLICK, вы соглашаетесь с настоящими правилами. Если вы с ними не согласны — пожалуйста, не пользуйтесь платформой.</p>

        <h2 className="text-lg font-bold text-gray-900">2. Требования к объявлениям</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>Объявления должны содержать актуальную и достоверную информацию об объекте аренды.</li>
          <li>Запрещено размещать дублирующиеся объявления, а также объявления не по теме аренды жилья.</li>
          <li>Фотографии должны соответствовать реальному состоянию объекта.</li>
          <li>Лимит: 10 объявлений в 24 часа на одного пользователя.</li>
        </ul>

        <h2 className="text-lg font-bold text-gray-900">3. Поведение пользователей</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>Запрещены оскорбления, спам и любые формы мошенничества.</li>
          <li>Пользователи несут ответственность за достоверность указанных контактных данных.</li>
          <li>Администрация вправе заблокировать аккаунт за нарушение правил.</li>
        </ul>

        <h2 className="text-lg font-bold text-gray-900">4. Ограничение ответственности</h2>
        <p>UY-CLICK является информационной площадкой. Мы не являемся стороной сделки между арендатором и арендодателем и не несём ответственности за качество услуг или споры между пользователями.</p>

        <h2 className="text-lg font-bold text-gray-900">5. Изменения правил</h2>
        <p>Мы вправе обновлять настоящие правила. О существенных изменениях мы уведомим пользователей через интерфейс платформы.</p>

        <p className="text-xs text-gray-400 mt-8">Последнее обновление: июнь 2025</p>
      </section>
    </div>
  );
}
