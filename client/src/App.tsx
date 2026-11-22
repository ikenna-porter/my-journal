import './App.css'


function App() {

  return (
    <>
    <form action="http://localhost:8080/entries/1" method="post">
      <input type="text" name="title" placeholder="Title" />
      <br />
      <textarea name="content" placeholder="Content"></textarea>
      <br />
      <input type="text" name="mood" placeholder="Mood" />
      <br />
      <button type="submit">Add Entry</button>
    </form>

    </>
  )
}

export default App
