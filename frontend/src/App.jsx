import { useState } from 'react'
import HelloWorld from './HelloWorld';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <HelloWorld />
    </>
  );
}

export default App
