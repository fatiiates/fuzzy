package com.fuzzy;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.URISyntaxException;
import java.text.NumberFormat;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;

import com.opencsv.CSVParser;
import com.opencsv.CSVParserBuilder;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.exceptions.CsvException;

import net.sourceforge.jFuzzyLogic.plot.JFuzzyChart;

/**
 * Hello world!
 *
 */
public class App {

    public static boolean chartsIsShowed = false;

    public static void main(String[] args) throws FileNotFoundException, IOException, CsvException, ParseException {
        try {
            CSVParser csvParser = new CSVParserBuilder().withSeparator(';').build();
            List<Double[]> rd = new ArrayList<Double[]>();
            try (CSVReader reader = new CSVReaderBuilder(new FileReader("src/main/resources/data.csv"))
                    .withCSVParser(csvParser).build()) {
                List<String[]> r = reader.readAll();
                Iterator<String[]> rIterator = r.iterator();
                rIterator.next(); // header bilgileri es geçiliyor
                while (rIterator.hasNext()) {

                    NumberFormat format = NumberFormat.getInstance(Locale.FRANCE);

                    rd.add(Arrays.stream(rIterator.next())
                            .map(x -> {
                                Number number = 0.0;
                                try {
                                    number = format.parse(x);
                                } catch (ParseException e) {
                                    e.printStackTrace();
                                }
                                return number.doubleValue();
                            })
                            .toArray(Double[]::new));

                }

            }

            for (int i = 0; i < rd.size(); i++) {
                Double[] cl = rd.get(i);
                rd.set(i, new Double[] { cl[0], cl[1], cl[2], cl[3], cl[4], App.calculateFuzzyVal(cl) });
            }
            Collections.sort(rd, new Comparator<Double[]>() {
                public int compare(Double[] o1, Double[] o2) {
                    Double pred = Math.abs(o1[4]-o1[5]);
                    Double pred2 = Math.abs(o2[4]-o2[5]);
                    return Double.compare(pred, pred2);
                }
            });
            Double mae = 0.0;
            Double rmse = 0.0;
            for (Double[] arr : rd) {
                App.printValues(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5]);

                mae += Math.abs(arr[4] - arr[5]);
                rmse += Math.pow(arr[4] - arr[5], 2);
            }
            mae /= rd.size();
            rmse /= rd.size();
            rmse = Math.sqrt(rmse);
            System.out.println("MAE => " + mae);
            System.out.println("RMSE => " + rmse);

        } catch (URISyntaxException ex) {
            System.out.println(ex.getMessage());
        }
    }

    private static Double calculateFuzzyVal(Double[] arr) throws URISyntaxException {
        FuzzyProject fz = new FuzzyProject(arr[0], arr[1], arr[2], arr[3]);
        if (!App.chartsIsShowed) {
            JFuzzyChart.get().chart(fz.getModel());
            App.chartsIsShowed = true;
        }

        return fz.toDouble();
    }

    private static void printValues(Double Iy, Double PF, Double e, Double dIf, Double If, Double guess) {
        System.out.print("Iy => " + Iy);
        System.out.print(", PF => " + PF);
        System.out.print(", e => " + e);
        System.out.print(", dIf => " + dIf);
        System.out.println(", Expected => " + If + ", gathered = " + guess);

    }

}
