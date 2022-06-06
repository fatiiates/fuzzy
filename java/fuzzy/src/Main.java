import java.net.URISyntaxException;
import net.sourceforge.jFuzzyLogic.plot.JFuzzyChart;

import com.opencsv.CSVReader;


public class Main {

	public static void main(String[] args) {
		try {
			System.out.println("TEST");
			FuzzyProject fz = new FuzzyProject(3, 0.66, 0.34, 0.383);
			System.out.println(fz);
			JFuzzyChart.get().chart(fz.getModel());
		} catch (URISyntaxException ex) {
			System.out.println(ex.getMessage());
		}
	}

}