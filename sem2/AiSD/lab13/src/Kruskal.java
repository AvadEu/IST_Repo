import java.util.Collections;
import java.util.List;

public class Kruskal {
    public static int findMST(int n, List<Edge> edges) {
        Collections.sort(edges);
        DisjointSetUnion dsu = new DisjointSetUnion(n);

        int totalWeight = 0;
        int edgesUsed = 0;

        for (Edge edge : edges) {
            if (dsu.union(edge.from, edge.to)) {
                totalWeight += edge.weight;
                edgesUsed++;
                if (edgesUsed == n - 1) break;
            }
        }

        return edgesUsed == n - 1 ? totalWeight : -1;
    }
}
