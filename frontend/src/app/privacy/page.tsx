import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Персональные данные · UY-CLICK',
  description: 'Политика обработки персональных данных платформы UY-CLICK.',
};

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Политика конфиденциальности</h1>

      <section className="space-y-4 text-sm text-gray-700 leading-relaxed">
        <h2 className="text-lg font-bold text-gray-900">1. Какие данные мы собираем</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li><strong>Email</strong> — при регистрации, используется для входа и уведомлений.</li>
          <li><strong>Данные объявлений</strong> — заголовок, район, цена, фото, координаты, телефон (если указан).</li>
          <li><strong>Сообщения</strong> — переписка в чате между пользователями.</li>
          <li><strong>Избранное</strong> — список объявлений, добавленных пользователем.</li>
        </ul>

        <h2 className="text-lg font-bold text-gray-900">2. Как мы используем данные</h2>
        <ul className="list-disc pl-5 space-y-1">
          <li>Для предоставления функций платформы: публикация объявлений, поиск, чат, карта.</li>
          <li>Для модерации: выявление и блокировка нарушителей правил.</li>
          <li>Для улучшения сервиса: агрегированная аналитика без привязки к конкретным пользователям.</li>
        </ul>

        <h2 className="text-lg font-bold text-gray-900">3. Хранение данных</h2>
        <p>Данные хранятся в Supabase (PostgreSQL) с соблюдением стандартов безопасности. Фотографии размещаются в Supabase Storage. Доступ к данным защищён Row-Level Security: каждый пользователь видит только свои данные.</p>

        <h2 className="text-lg font-bold text-gray-900">4. Передача третьим лицам</h2>
        <p>Мы не продаём и не передаём персональные данные третьим лицам. Исключение — требования законодательства Республики Узбекистан.</p>

        <h2 className="text-lg font-bold text-gray-900">5. Удаление данных</h2>
        <p>Вы можете удалить свои объявления в разделе «Мои объявления». Для полного удаления аккаунта и всех связанных данных — свяжитесь с нами через раздел поддержки.</p>

        <h2 className="text-lg font-bold text-gray-900">6. Файлы cookie</h2>
        <p>Мы используем localStorage для хранения токена авторизации и языковых предпочтений. Сторонние трекинговые cookie не используются.</p>

        <p className="text-xs text-gray-400 mt-8">Последнее обновление: июнь 2025</p>
      </section>
    </div>
  );
}
