import type { SearchResult } from "./types";
import { Paper,Title,Text ,Group, Badge,Anchor} from "@mantine/core"
function ResultList({ results }: { results: SearchResult[] }) {
    return  results.map(r => (<Paper withBorder shadow="xl" radius="md" p="md" key={`${r.file_name}-${r.chunk_number}`}><Group justify="space-between"><Title order={4}><Anchor href={`https://arxiv.org/abs/${r.file_name.replace(".pdf", "")}`} target="_blank">
    {r.file_name}
  </Anchor> Chunk: {r.chunk_number}</Title> </Group> cosinus similarity: <Badge>{ r.score.toFixed(3)}</Badge> bonus+ {r.bonus!==undefined && ( <Badge color="green">{r.bonus.toFixed(3)}</Badge>) }  <Text size={"sm"} c={"dimmed"} lineClamp={3}> {r.text.slice(0, 300)}</Text> </Paper>))
}


export default ResultList