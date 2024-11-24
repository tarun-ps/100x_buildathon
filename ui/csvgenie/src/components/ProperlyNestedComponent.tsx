export function ProperlyNestedComponent() {
  return (
    <section className="p-8 bg-purple-400 text-white rounded-lg shadow-lg">
      <header className="mb-4">
        <h1 className="text-2xl">Nested Component</h1>
      </header>
      <article className="space-y-4">
        <p>Content within a properly nested component.</p>
        <button className="bg-purple-700 px-4 py-2 rounded hover:bg-purple-800">
          Learn More
        </button>
      </article>
    </section>
  )
} 