import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.StreamTokenizer;

class Main {
    public static void main(String[] args) throws IOException {
        StreamTokenizer in = new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in)));

        in.nextToken();
        int n = (int) in.nval;

        in.nextToken();
        long value = (long) in.nval;
        long smallest = value;
        long largest = value;

        for (int i = 1; i < n; i++) {
            in.nextToken();
            value = (long) in.nval;
            if (value < smallest) smallest = value;
            if (value > largest) largest = value;
        }

        System.out.print(largest - smallest);
    }
}
