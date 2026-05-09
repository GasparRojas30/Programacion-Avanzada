package org.example;
import java.util.*;

public class HashingLab {
    static class Pair {
        String key;
        int value;
        Pair(String key, int value) {
            this.key   = key;
            this.value = value;
        }
    }

    static class HashTableChaining {
        private final List<List<Pair>> table;
        private final int    size;
        private final String hashStrategy;
        private int count;
        private int collisions;

        public HashTableChaining(int size, String hashStrategy) {
            this.size         = size;
            this.hashStrategy = hashStrategy;
            this.count        = 0;
            this.collisions   = 0;
            this.table        = new ArrayList<>(size);
            for (int i = 0; i < size; i++) {
                table.add(new LinkedList<>());
            }
        }

        private int hashSum(String key) {
            int sum = 0;
            for (int i = 0; i < key.length(); i++) {
                sum += key.charAt(i);
            }
            return Math.floorMod(sum, size);
        }

        private int hashPolynomial(String key) {
            int h    = 0;
            int base = 31;
            for (int i = 0; i < key.length(); i++) {
                h = Math.floorMod(h * base + key.charAt(i), size);
            }
            return h;
        }

        private int hash(String key) {
            switch (hashStrategy) {
                case "sum":        return hashSum(key);
                case "polynomial": return hashPolynomial(key);
                default: throw new IllegalArgumentException(
                        "Estrategia desconocida: " + hashStrategy);
            }
        }

        public void insert(String key, int value) {
            int idx = hash(key);
            List<Pair> bucket = table.get(idx);

            for (Pair p : bucket) {
                if (p.key.equals(key)) {
                    p.value = value;
                    return;
                }
            }
            if (!bucket.isEmpty()) {
                collisions++;
            }
            bucket.add(new Pair(key, value));
            count++;
        }

        public Integer search(String key) {
            int idx = hash(key);
            for (Pair p : table.get(idx)) {
                if (p.key.equals(key)) return p.value;
            }
            return null;
        }

        public boolean delete(String key) {
            int idx = hash(key);
            List<Pair> bucket = table.get(idx);
            Iterator<Pair> it = bucket.iterator();
            while (it.hasNext()) {
                if (it.next().key.equals(key)) {
                    it.remove();
                    count--;
                    return true;
                }
            }
            return false;
        }

        public double loadFactor() {
            return (double) count / size;
        }

        public int usedBuckets() {
            int used = 0;
            for (List<Pair> b : table) if (!b.isEmpty()) used++;
            return used;
        }

        public int maxBucketSize() {
            int max = 0;
            for (List<Pair> b : table) max = Math.max(max, b.size());
            return max;
        }

        public Map<Integer, Integer> bucketSizeDistribution() {
            Map<Integer, Integer> dist = new TreeMap<>();
            for (List<Pair> b : table) {
                int sz = b.size();
                dist.merge(sz, 1, Integer::sum);
            }
            return dist;
        }

        public void printReport(String datasetName, double elapsedSeconds) {
            String label = hashStrategy.equals("sum") ? "Suma" : "Polinomial";

            System.out.println("Hash: " + label);
            System.out.println("Dataset: " + datasetName);
            System.out.println("Tamaño de tabla (m): " + size);
            System.out.println("Elementos insertados: " + count);
            System.out.println("Factor de carga (n/m): " + String.format("%.4f", loadFactor()));
            System.out.println("Colisiones: " + collisions);
            System.out.println("Buckets usados: " + usedBuckets());
            System.out.println("Tamaño máximo de bucket: " + maxBucketSize());
            System.out.println("Tiempo de inserción (s): " + String.format("%.6f", elapsedSeconds));
            System.out.println();
        }
    }

    static List<String> generateRandomKeys(int n, int length) {
        Random rng = new Random(42);
        List<String> keys = new ArrayList<>(n);
        String alphabet = "abcdefghijklmnopqrstuvwxyz";
        for (int i = 0; i < n; i++) {
            StringBuilder sb = new StringBuilder(length);
            for (int j = 0; j < length; j++) {
                sb.append(alphabet.charAt(rng.nextInt(alphabet.length())));
            }
            keys.add(sb.toString());
        }
        return keys;
    }

    static List<String> generateSequentialKeys(int n) {
        List<String> keys = new ArrayList<>(n);
        for (int i = 0; i < n; i++) keys.add("user" + i);
        return keys;
    }

    static List<String> generateClusteredKeys(int n) {
        List<String> keys = new ArrayList<>(n);
        for (int i = 0; i < n; i++) keys.add("aaa" + i);
        return keys;
    }

    static void runExperiment(String datasetName, List<String> keys, int tableSize) {
        for (String strategy : Arrays.asList("sum", "polynomial")) {
            HashTableChaining ht = new HashTableChaining(tableSize, strategy);

            long start = System.nanoTime();
            for (int i = 0; i < keys.size(); i++) {
                ht.insert(keys.get(i), i);
            }
            long end = System.nanoTime();

            double elapsedSeconds = (end - start) / 1_000_000_000.0;
            ht.printReport(datasetName, elapsedSeconds);
        }
    }

    public static void main(String[] args) {
        int n         = 1000;
        int tableSize = 211;

        System.out.println("=== LABORATORIO DE TABLAS HASH CON ENCADENAMIENTO ===");
        System.out.println("n=" + n + " claves | m=" + tableSize + " (primo) | Chaining");
        System.out.println();

        runExperiment("Aleatorio (strings random de largo 8)",
                generateRandomKeys(n, 8), tableSize);
        runExperiment("Secuencial (user0...user999)",
                generateSequentialKeys(n), tableSize);
        runExperiment("Agrupado (aaa0...aaa999)",
                generateClusteredKeys(n), tableSize);
    }
}