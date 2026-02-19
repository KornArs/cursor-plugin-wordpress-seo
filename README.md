# WordPress SEO Publisher — Cursor Plugin

Плагин для Cursor 2.5: создание постов, публикация в WordPress и анализ SEO & GEO.

## Возможности

- **Создание постов** — генерация и редактирование контента
- **Публикация в WordPress** — через MCP (REST API)
- **SEO-анализ** — ключевые слова, заголовки H1–H3, плотность, рекомендации
- **GEO-анализ** — упоминания локаций, оценка локального SEO

## Установка

### 1. Установка плагина

```bash
# Через Cursor: /add-plugin и укажите URL репозитория
# Например: https://github.com/YOUR_USERNAME/cursor-plugin-wordpress-seo
```

### 2. Настройка WordPress

**Вариант A: MCP Adapter (рекомендуется)**

1. Установите [WordPress MCP Adapter](https://github.com/WordPress/mcp-adapter) на сайт
2. Включите MCP в Настройки → MCP Settings

**Вариант B: Application Passwords**

1. WordPress 5.6+: Users → Profile → Application Passwords
2. Создайте пароль для «Cursor» или «MCP»

### 3. Переменные окружения

Добавьте в настройки MCP Cursor (или `.env`):

```json
{
  "WP_API_URL": "https://your-wordpress-site.com"
}
```

Для Application Passwords (без OAuth):

```json
{
  "WP_API_URL": "https://yoursite.com",
  "WP_API_USERNAME": "admin",
  "WP_API_PASSWORD": "xxxx xxxx xxxx xxxx",
  "OAUTH_ENABLED": "false"
}
```

## Использование

### Создание и публикация поста

1. Попросите агента создать пост по теме
2. Агент использует WordPress MCP для публикации
3. Или вручную: `POST /wp-json/wp/v2/posts` с Basic Auth

### SEO & GEO анализ

```bash
# Анализ файла
python scripts/analyze-seo-geo.py post.md --keywords "keyword1,keyword2" --location "Москва"

# Из stdin
cat post.html | python scripts/analyze-seo-geo.py - --keywords "seo"
```

## Структура плагина

```
cursor-plugin-wordpress-seo/
├── .cursor-plugin/
│   └── plugin.json
├── mcp.json              # WordPress MCP config
├── skills/
│   └── wordpress-seo-publisher/
│       └── SKILL.md
├── rules/
│   └── wordpress-workflow.mdc
├── scripts/
│   └── analyze-seo-geo.py
├── assets/
│   └── logo.svg
└── README.md
```

## Ссылки

- [Cursor 2.5 Plugins](https://forum.cursor.com/t/cursor-2-5-plugins/152124)
- [cursor/plugin-template](https://github.com/cursor/plugin-template)
- [@automattic/mcp-wordpress-remote](https://www.npmjs.com/package/@automattic/mcp-wordpress-remote)
- [WordPress REST API](https://developer.wordpress.org/rest-api/)
