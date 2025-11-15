import java.io.*;

public class FileParser {
    public static void parseFile(String filename, RBTree tree) throws IOException {
        BufferedReader br = new BufferedReader(new FileReader(filename));

        String line;
        int lineNumber = 1;

        while ((line = br.readLine()) != null) {

            String[] words = line.toLowerCase().split("[^a-ząćęłńóśżź]+");

            for (String word : words) {
                if (!word.isBlank()) {
                    tree.insert(word, lineNumber);
                }
            }
            lineNumber++;
        }

        br.close();
    }
}
