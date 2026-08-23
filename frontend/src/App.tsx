import './App.css'
import { useState } from 'react'
import { TextInput, Button, Checkbox, Stack, Paper } from '@mantine/core';
interface SearchResult {
  text: String;
  file_name: String;
  chunk_number: number;
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
  const [error, setError] = useState<string | null>(null);
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
      <TextInput value={chunkSize} onChange={e => setChunkSize(e.target.value)} placeholder="Chunksize" label="Chunksize (200-650)" />
      <TextInput value={terms} onChange={e => setTerms(e.target.value)} placeholder='Terminology' label="Terminology" />
      <TextInput value={bonus} onChange={e => setBonus(e.target.value)} placeholder="Bonus" label="Bonus" />

      <Button onClick={handleSearch} disabled={!query.trim() || loading}> Search</Button>

      <div> {loading ? <p>Searching...</p> : results.map(r => (<Paper withBorder shadow="xl" radius="md" p="md"  key={`${r.file_name}-${r.chunk_number}`}><h3>{r.file_name} Chunk: {r.chunk_number} cosinus similarity:{r.score.toFixed(3)} bonus +{r.bonus.toFixed(3)} </h3><p> {r.text.slice(0, 300)}</p> </Paper>))} </div>
      {error && <p role="alert" style={{ color: "red" }}> {error} </p>}
    </Stack>




  )
}

export default App
