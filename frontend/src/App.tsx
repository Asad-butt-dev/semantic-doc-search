import './App.css'
import { useState } from 'react'
import { TextInput, Button, Checkbox, Stack, Title, Text, Anchor, Chip, Group } from '@mantine/core';
import "./ResultList"
import type { SearchResult } from "./types"
import ResultList from './ResultList';
import.meta.env
const API_URL = "/api";
function App() {
  const [query, setQuery] = useState("");
  const [hybrid, setHybrid] = useState(false);
  const [terms, setTerms] = useState("")
  const [results, setResults] = useState<SearchResult[]>([]);
  const [bonus, setBonus] = useState("0");
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null);
  const examples = [
  "What are PLM-based Rerankers?",
  "How does the quality of data annotation influence scaling effects?",
  "How does the process begin when adapting a retrieval model to a new domain without labels?",
];
  async function handleSearch() {
    const termList = terms.split(",").map(a => a.trim())
    const params = new URLSearchParams({ query: query, use_hybrid: String(hybrid), bonus: bonus })
    for (let i = 0; i < termList.length; i++) {
      params.append("key_terms", termList[i]);
    }
    const url = API_URL + "/search?" + params;

    try {
      setLoading(true);
      setError(null)
      const answer = await fetch(url);
      if (!answer.ok) {
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
      <Title order={1}>Semantic Document Search</Title>
      <Text c="dimmed" size="sm">
        Demo interface. The core of this project is the retrieval evaluation — see the README for methodology, metrics and findings.
      </Text>
      <Anchor href="https://github.com/Asad-butt-dev/semantic-doc-search#evaluation" size="sm">
        See evaluation results →
      </Anchor>
      <TextInput value={query} onChange={e => setQuery(e.target.value)} placeholder="Search..."
        label="Query" />
      <Checkbox checked={hybrid} onChange={e => setHybrid(e.target.checked)} placeholder='Hybrid' label="HybridSearch" />
      <TextInput value={terms} onChange={e => setTerms(e.target.value)} placeholder='Terminology' label="Terminology" />
      <TextInput value={bonus} onChange={e => setBonus(e.target.value)} placeholder="Bonus" label="Bonus (0.1-0.3)" />
      <Text c="dimmed">Example queries</Text>
      <Chip.Group value={query} onChange={setQuery}>
        <Group>
          {examples.map(q => (
            <Chip key={q} value={q}>{q}</Chip>
          ))}
        </Group>
      </Chip.Group>

      <Button onClick={handleSearch} disabled={!query.trim() || loading}> Search</Button>

      <div> {loading ? <p>Searching...</p> : <ResultList results={results} />}</div>
      {error && <p role="alert" style={{ color: "red" }}> {error} </p>}
    </Stack>




  )
}

export default App
