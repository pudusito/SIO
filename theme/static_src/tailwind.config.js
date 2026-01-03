module.exports = {
    content: [
        // Templates within theme app (e.g. base.html)
        '../templates/**/*.html',
        '../templates/*.html',
        '../../apps/**/*.html',
        // Templates in other apps
        '../../templates/**/*.html',
            "../../apps/**/templates/**/*.html",
        "../../apps/**/templates/**/*.js",   // si tienes js con clases tailwind
        "../../templates/**/*.html",         // si usas carpeta templates global
        "./templates/**/*.html",             // templates dentro del theme
        // Ignore files in node_modules
        '!../../**/node_modules',
        '!../**/node_modules', 
        // Include JavaScript files that might contain Tailwind CSS classes
        '../../**/*.js',
        // Include Python files that might contain Tailwind CSS classes
        '../../**/*.py'
    ],
        theme: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}