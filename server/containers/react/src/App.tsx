import { useState } from 'react'


function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div className='container'>
        <h1>React</h1>
        <img src="https://cdn.worldvectorlogo.com/logos/react-2.svg" alt="react" className="logo" />
        <p>{count}</p>
        <button onClick={() => setCount(count + 1)}>Click me</button>
        </div>
    </>
  )
}

export default App
