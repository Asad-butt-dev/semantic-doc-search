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
  const [loading, setLoading] = useState(false)
  const [error,setError]=useState<string|null>(null);
  async function handleSearch() {
    const termList = terms.split(",").map(a => a.trim())
    const params = new URLSearchParams({ query: query, use_hybrid: String(hybrid), chunk_size: chunkSize, bonus: bonus })
    for (let i = 0; i < termList.length; i++) {
      params.append("key_terms", termList[i]);
    }
    const url = "http://127.0.0.1:8000/search?" + params;
  
    try {
      setLoading(true);
      setError(null)
      const answer = await fetch(url);
      if (answer.status != 200) {
        throw new Error(answer.status.toString())
      }
    const data = await answer.json();
    setResults(data);

    } catch (error) {
     setError("Could not reach the server");
     console.log(error);
    setResults([]);
    }
    finally{

    setLoading(false);
    }
  }

  return (
    <div>
      <input type="text" placeholder='Input' value={query} onChange={e => setQuery(e.target.value)} />
      <input type='text' placeholder='Chunksize' value={chunkSize} onChange={e => setChunkSize(e.target.value)} />
      <input type="checkbox" checked={hybrid} onChange={e => setHybrid(e.target.checked)} /> <label>HybridSearch</label>
      <input type='text' placeholder='Terminology' value={terms} onChange={e => setTerms(e.target.value)} />
      <input type="text" placeholder='bonus' value={bonus} onChange={e => setBonus(e.target.value)}  />
      <button onClick={handleSearch} disabled={!query.trim()||loading}> Search </button>
      <div> {loading ? <p>Searching...</p> : results.map(r => (<div key={`${r.fileName}-${r.chunkNumber}`}><h3>{r.fileName} Chunk: {r.chunkNumber} cosinus similarity:{r.score.toFixed(3)} bonus +{r.bonus} </h3><p> {r.text.slice(0, 300)}</p> </div>))} </div>
    { error && <p  role="alert" style={{color:"red"}}> {error} </p>}
    </div>
    
  )
}

export default App
