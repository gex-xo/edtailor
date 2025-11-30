// EdTailor - Fashion Education Platform
// Alpine.js Application Logic

const API_BASE_URL = 'http://localhost:8000/api';

function app() {
    return {
        // State
        currentView: 'home',
        language: 'en',
        categories: [],
        topics: [],
        lessons: [],
        fabrics: [],
        garments: [],
        terms: [],
        selectedCategory: null,
        selectedTopic: null,
        selectedLesson: null,

        // Initialization
        async init() {
            // Load language from localStorage
            const savedLanguage = localStorage.getItem('edtailor_language');
            if (savedLanguage) {
                this.language = savedLanguage;
            }

            // Load initial data
            await this.loadCategories();
        },

        // Language Management
        async changeLanguage() {
            localStorage.setItem('edtailor_language', this.language);

            // Reload current view data
            switch(this.currentView) {
                case 'home':
                    await this.loadCategories();
                    break;
                case 'topics':
                    if (this.selectedCategory) {
                        await this.loadTopics(this.selectedCategory.id);
                    }
                    break;
                case 'lessons':
                    if (this.selectedTopic) {
                        await this.loadLessons(this.selectedTopic.id);
                    }
                    break;
                case 'fabrics':
                    await this.loadFabrics();
                    break;
                case 'garments':
                    await this.loadGarments();
                    break;
                case 'glossary':
                    await this.loadTerms();
                    break;
            }
        },

        // Navigation
        goHome() {
            this.currentView = 'home';
            this.selectedCategory = null;
            this.selectedTopic = null;
            this.selectedLesson = null;
            this.loadCategories();
        },

        backToTopics() {
            this.currentView = 'topics';
            this.selectedLesson = null;
        },

        backToLessons() {
            this.currentView = 'lessons';
            this.selectedLesson = null;
        },

        // API Calls - Categories
        async loadCategories() {
            try {
                const response = await fetch(`${API_BASE_URL}/categories?language=${this.language}`);
                if (!response.ok) throw new Error('Failed to load categories');
                this.categories = await response.json();
            } catch (error) {
                console.error('Error loading categories:', error);
                this.categories = [];
            }
        },

        async selectCategory(category) {
            this.selectedCategory = category;
            this.currentView = 'topics';
            await this.loadTopics(category.id);
        },

        // API Calls - Topics
        async loadTopics(categoryId) {
            try {
                const response = await fetch(`${API_BASE_URL}/categories/${categoryId}/topics?language=${this.language}`);
                if (!response.ok) throw new Error('Failed to load topics');
                this.topics = await response.json();
            } catch (error) {
                console.error('Error loading topics:', error);
                this.topics = [];
            }
        },

        async selectTopic(topic) {
            this.selectedTopic = topic;
            this.currentView = 'lessons';
            await this.loadLessons(topic.id);
        },

        // API Calls - Lessons
        async loadLessons(topicId) {
            try {
                const response = await fetch(`${API_BASE_URL}/topics/${topicId}/lessons?language=${this.language}`);
                if (!response.ok) throw new Error('Failed to load lessons');
                this.lessons = await response.json();
            } catch (error) {
                console.error('Error loading lessons:', error);
                this.lessons = [];
            }
        },

        async viewLesson(lesson) {
            try {
                // Fetch full lesson details including content
                const response = await fetch(`${API_BASE_URL}/lessons/${lesson.id}`);
                if (!response.ok) throw new Error('Failed to load lesson details');
                this.selectedLesson = await response.json();
                this.currentView = 'lesson-detail';
            } catch (error) {
                console.error('Error loading lesson:', error);
            }
        },

        // API Calls - Fabrics
        async loadFabrics() {
            try {
                const response = await fetch(`${API_BASE_URL}/fabrics?language=${this.language}`);
                if (!response.ok) throw new Error('Failed to load fabrics');
                this.fabrics = await response.json();
            } catch (error) {
                console.error('Error loading fabrics:', error);
                this.fabrics = [];
            }
        },

        // API Calls - Garments
        async loadGarments() {
            try {
                const response = await fetch(`${API_BASE_URL}/garments?language=${this.language}`);
                if (!response.ok) throw new Error('Failed to load garments');
                this.garments = await response.json();
            } catch (error) {
                console.error('Error loading garments:', error);
                this.garments = [];
            }
        },

        // API Calls - Terms
        async loadTerms() {
            try {
                const response = await fetch(`${API_BASE_URL}/terms?language=${this.language}`);
                if (!response.ok) throw new Error('Failed to load terms');
                this.terms = await response.json();
            } catch (error) {
                console.error('Error loading terms:', error);
                this.terms = [];
            }
        },

        // Markdown formatting
        formatMarkdown(content) {
            if (!content) return '';

            // Simple markdown parser for lesson content
            let html = content;

            // Headers
            html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
            html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
            html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

            // Bold
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');

            // Italic
            html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
            html = html.replace(/_(.*?)_/g, '<em>$1</em>');

            // Lists
            html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
            html = html.replace(/^\- (.*$)/gim, '<li>$1</li>');
            html = html.replace(/^(\d+)\. (.*$)/gim, '<li>$2</li>');

            // Wrap consecutive <li> in <ul>
            html = html.replace(/(<li>.*<\/li>\n?)+/g, (match) => {
                return '<ul>' + match + '</ul>';
            });

            // Paragraphs
            html = html.split('\n\n').map(paragraph => {
                if (paragraph.trim() &&
                    !paragraph.startsWith('<h') &&
                    !paragraph.startsWith('<ul') &&
                    !paragraph.startsWith('<ol') &&
                    !paragraph.startsWith('<li')) {
                    return '<p>' + paragraph.trim() + '</p>';
                }
                return paragraph;
            }).join('\n');

            // Line breaks
            html = html.replace(/\n/g, '<br>');

            return html;
        }
    };
}
