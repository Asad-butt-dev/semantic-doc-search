import './App.css'
import { useState } from 'react'
interface SearchResult {
  text: String;
  fileName: String;
  chunkNumber: number;
  score: number;
  bonus: number;

}

function App() {
  const [query, setQuery] = useState("");
  const [chunkSize, setChunkSize] = useState("500");
  const [hybrid, setHybrid] = useState(false);
  const [terms, setTerms] = useState("")
  const [results, setResults] = useState<SearchResult[]>([]);
  const [bonus, setBonus] = useState("0");

  async function handleSearch() {
    const termList = terms.split(",").map(a => a.trim())
    const params = new URLSearchParams({ qu: query, hs: String(hybrid), ch: chunkSize, bo: bonus })
    for (let i = 0; i < termList.length; i++) {
      params.append("te", termList[i]);
    }
    const url = "http://127.0.0.1:8000/search?" + params
    const answer = await fetch(url);
    const data = await answer.json();
    setResults(data);
  }

  return (
    <div>
      <input type="text" placeholder='Input' value={query} onChange={e => setQuery(e.target.value)} />
      <input type='text' placeholder='Chunksize' value={chunkSize} onChange={e => setChunkSize(e.target.value)} />
      <input type="checkbox" checked={hybrid} onChange={e => setHybrid(e.target.checked)} /> <label>HybridSearch</label>
      <input type='text' placeholder='Terminology' value={terms} onChange={e => setTerms(e.target.value)} />
      <input type="text" placeholder='bonus' value={bonus} onChange={e => setBonus(e.target.value)} />
      <button onClick={handleSearch}> Search </button>
      <div>{results.map(r => (<div key={`${r.fileName}-${r.chunkNumber}`}><h3>{r.fileName} Chunk: {r.chunkNumber} cosinus similarity:{r.score.toFixed(3)} bonus +{r.bonus} </h3><p> {r.text.slice(0, 300)}</p> </div>))} </div>
    </div>
  )
}

export default App
