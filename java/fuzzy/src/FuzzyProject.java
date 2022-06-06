import java.io.File;
import java.net.URISyntaxException;
import net.sourceforge.jFuzzyLogic.FIS;

public class FuzzyProject {
    
    private final FIS fis;
    private final double IyRate;
    private final double PFRate;
    private final double eRate;
    private final double dIfRate;

    public FuzzyProject(double IyRate, double PFRate, double eRate, double dIfRate) throws URISyntaxException {
        this.IyRate = IyRate;
        this.PFRate = PFRate;
        this.eRate = eRate;
        this.dIfRate = dIfRate;
        fis = FIS.load("/home/tati/github/fuzzy/java/fuzzy/src/FuzzyProjectModel.fcl", true);
        fis.setVariable("IyRate", IyRate);
        fis.setVariable("PFRate", PFRate);
        fis.setVariable("eRate", eRate);
        fis.setVariable("dIfRate", dIfRate);
        fis.evaluate();
    }

    public FIS getModel() {
        return fis;
    }

    @Override
    public String toString() {
        String output = "If Rate :" + fis.getVariable("IfRate").getValue();
        return output;
    }

}
