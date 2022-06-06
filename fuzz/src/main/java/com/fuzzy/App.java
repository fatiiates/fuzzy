package com.fuzzy;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.net.URISyntaxException;
import java.text.NumberFormat;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;

import net.sourceforge.jFuzzyLogic.plot.JFuzzyChart;

import com.opencsv.CSVParser;
import com.opencsv.CSVParserBuilder;
import com.opencsv.CSVReader;
import com.opencsv.CSVReaderBuilder;
import com.opencsv.exceptions.CsvException;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args ) throws FileNotFoundException, IOException, CsvException, ParseException
    {
        try {
            CSVParser csvParser = new CSVParserBuilder().withSeparator(';').build();
            List<Double[]> rd = new ArrayList<Double[]>();
            try (CSVReader reader = new CSVReaderBuilder(new FileReader("src/main/resources/data.csv"))
                .withCSVParser(csvParser).build()
            ) {
                List<String[]> r = reader.readAll();
                Iterator<String[]> countriesIterator = r.iterator();
                countriesIterator.next(); // header bilgileri es geçiliyor
                while (countriesIterator.hasNext()) {
                    
                    NumberFormat format = NumberFormat.getInstance(Locale.FRANCE);
                    
                    rd.add(Arrays.stream(countriesIterator.next())
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
            List<Double[]> results = new ArrayList<Double[]>();
            for (Double[] d : rd) 
                results.add(new Double[]{d[4], App.calculateFuzzyVal(d)});
            Double mae = 0.0;
            Double rmse = 0.0;
            for (Double[] res : results) {
                mae += Math.abs(res[0] - res[1]);
                rmse += Math.pow(res[0] - res[1], 2);
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

    private static Double calculateFuzzyVal(Double[] arr) throws URISyntaxException{
        FuzzyProject fz = new FuzzyProject(arr[0],arr[1],arr[2],arr[3]);
        // System.out.println(fz);
        // JFuzzyChart.get().chart(fz.getModel());

        return fz.toDouble();
    }

}
