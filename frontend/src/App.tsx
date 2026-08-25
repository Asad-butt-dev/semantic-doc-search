import './App.css'
import { useState } from 'react'
import { TextInput, Button, Checkbox, Stack,} from '@mantine/core';
import "./ResultList"
import  type {SearchResult} from "./types"
import ResultList from './ResultList';
import.meta.env 
const API_URL = import.meta.env.VITE_API_URL;
function App() {
  const [query, setQuery] = useState("");
  const [hybrid, setHybrid] = useState(false);
  const [terms, setTerms] = useState("")
  const [results, setResults] = useState<SearchResult[]>([]);
  const [bonus, setBonus] = useState("0");
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null);
  async function handleSearch() {
    const termList = terms.split(",").map(a => a.trim())
    const params = new URLSearchParams({ query: query, use_hybrid: String(hybrid), bonus: bonus })
    for (let i = 0; i < termList.length; i++) {
      params.append("key_terms", termList[i]);
    }
    const url = API_URL+"/search?"+ params;
    
    try {
      setLoading(true);
      setError(null)
      const answer = await fetch(url);
      if (!answer.ok ) {
        setError(`Search failed with status ${answer.status}`);
        return;
      }
      const data = await answer.json();
      setResults(data);

    } catch (error) {
      setError("Could not reach the Server");
      console.error(error);
      setResults([]);
    }
    finally {

      setLoading(false);
    }
  }

  return (


    <Stack 
      gap="md">
        <TextInput value={query} onChange={e => setQuery(e.target.value)} placeholder="Search..."
        label="Query" />
      <Checkbox checked={hybrid} onChange={e => setHybrid(e.target.checked)} placeholder='Hybrid' label="HybridSearch" />
      <TextInput value={terms} onChange={e => setTerms(e.target.value)} placeholder='Terminology' label="Terminology" />
      <TextInput value={bonus} onChange={e => setBonus(e.target.value)} placeholder="Bonus" label="Bonus (0.1-0.3)" />

      <Button onClick={handleSearch} disabled={!query.trim() || loading}> Search</Button>

      <div> {loading ? <p>Searching...</p> :<ResultList results={results}/> }</div>
      {error && <p role="alert" style={{ color: "red" }}> {error} </p>}
    </Stack>




  )
}

export default App
