/*
 * Generates aerodynamic deck
 * Author: Carter Tegen
 * Written: December 2022
 */
package macro;
import java.util.*;
import java.io.*;
import star.common.*;
import star.base.neo.*;
import star.material.*;
import star.resurfacer.*;
import star.coupledflow.*;
import star.vis.*;
import star.flow.*;
import star.energy.*;
import star.metrics.*;
import star.meshing.*;
import star.mapping.*;

import java.time.format.DateTimeFormatter;  
import java.time.LocalDateTime;    

public class generateDeck extends StarMacro {

    static double[] machArray = {0.1, 0.3, 0.7, 0.9, 0.95, 0.99, 1, 1.05, 1.3, 1.6, 2};
    static double[] aoaArray = {-2, -1, 0, 1, 2, 3, 5, 7, 9, 11};
    static double[] betaArray = {0};
    
    
    int count = 1;
    int numIters = machArray.length * aoaArray.length * betaArray.length;

    final double TREF = 288.15;
    final double SREF = 39.58; //m2
    final double SVTREF = 5.92; //m2
    final double RHOREF = 1.225; //kg/m3
    final double aRef = 340;

    Simulation sim;

    String fileOut = "Fine_NoRefinement_Results";

    public void execute() {

        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");  
        LocalDateTime now = LocalDateTime.now();  
        System.out.println(dtf.format(now)); 

        sim = getActiveSimulation();
        try {
            PrintWriter out = new PrintWriter(new FileWriter(new File(resolvePath(fileOut + ".csv"))));
            out.println("Mach, Beta, AOA, Lift, Drag, Moment, L/D, CL, CD");

        
            for(double mach : machArray) {
                for(double beta : betaArray) {
                    updateParameters(calculateFlowAngle(aoaArray[0], betaArray[0]), mach);
                    
                    for(double aoa : aoaArray) {

                        sim.println(String.format("---On run %d of %d---", count, numIters));
                        
                        double[] flowAngle = calculateFlowAngle(aoa, beta);
                        //sim.println("Updating parameters");
                        updateParameters(flowAngle, mach);
                        initialize();
                        //sim.println("Running case");
                        runCase();

                        //sim.println("Printing output");
                        printOutput(out, mach, aoa, beta);

                        count++;
                    }
                }
            }

            out.close();
        } catch (Exception e) {
            
            sim.println("Error in execute");
        }        
    }

    //Updates the farfield parameters to new Mach number and flow direction
    public void updateParameters(double[] flowAngle, double mach) {
        PhysicsContinuum physicsContinuum_0 = 
        ((PhysicsContinuum) sim.getContinuumManager().getContinuum("Physics 1"));

        VelocityProfile velocityProfile_0 = 
        physicsContinuum_0.getInitialConditions().get(VelocityProfile.class);

        Units units_4 = 
        ((Units) sim.getUnitsManager().getObject("m/s"));

        double xVelocity = mach*aRef*flowAngle[0];
        double yVelocity = mach*aRef*flowAngle[1];
        double zVelocity = mach*aRef*flowAngle[2];


        velocityProfile_0.getMethod(ConstantVectorProfileMethod.class).getQuantity().setComponentsAndUnits(xVelocity, yVelocity, zVelocity, units_4);
        Region region_0 = sim.getRegionManager().getRegion("fluid");
        Boundary boundary_1 = region_0.getBoundaryManager().getBoundary("farfield");
        FlowDirectionProfile flowDirectionProfile_0 = boundary_1.getValues().get(FlowDirectionProfile.class);
        Units units_3 = ((Units) sim.getUnitsManager().getObject(""));
        flowDirectionProfile_0.getMethod(ConstantVectorProfileMethod.class).getQuantity().setComponentsAndUnits(flowAngle[0], flowAngle[1], flowAngle[2], units_3);
        MachNumberProfile machNumberProfile_0 = boundary_1.getValues().get(MachNumberProfile.class);
        machNumberProfile_0.getMethod(ConstantScalarProfileMethod.class).getQuantity().setValueAndUnits(mach, units_3);
    }

    //Runs the simulation
    public void runCase() {
        Simulation sim = 
        getActiveSimulation();

        Solution solution_0 = 
        sim.getSolution();

        sim.getSimulationIterator().run();
    }

    //Initializes the simulation
    public void initialize() {
        Simulation sim = 
        getActiveSimulation();

        Solution solution_0 = 
        sim.getSolution();

        solution_0.clearSolution();

        solution_0.initializeSolution();
    }

    /*
     * Outputs line of data to csv
     */
    public void printOutput(PrintWriter fr, double mach, double aoa, double beta) {
        Simulation sim = getActiveSimulation();
        ForceReport forceReport_2 = ((ForceReport) sim.getReportManager().getReport("Axial Force"));
        MomentReport momentReport_1 = ((MomentReport) sim.getReportManager().getReport("Rotation Moment"));
        ForceReport forceReport_1 = ((ForceReport) sim.getReportManager().getReport("Normal Force"));

        sim.println("Getting monitored values");
        double normalForce = forceReport_1.monitoredValue();
        double axialForce = forceReport_2.monitoredValue();
        double moment = momentReport_1.monitoredValue();

        sim.println("Got monitored values");
        double caoa = Math.cos(Math.toRadians(aoa));
        double saoa = Math.sin(Math.toRadians(aoa));
        double cbeta = Math.cos(Math.toRadians(beta));
        double sbeta = Math.sin(Math.toRadians(beta));

        double lift = normalForce * caoa - axialForce * saoa * cbeta;
        double drag = axialForce * caoa * cbeta + normalForce * saoa;

        double CL = lift/(0.5 * RHOREF * Math.pow((mach * aRef), 2) * SREF);
        double CD = drag/(0.5 * RHOREF * Math.pow((mach * aRef), 2) * SREF);

        sim.println("Calculated lift and drag");

        //Mach, Beta, AOA, Lift, Drag, Moment, L/D
        String outString = String.format("%f, %f, %f, %f, %f, %f, %f, %f, %f",
            mach, beta, aoa, lift, drag, moment, lift/drag, CL, CD);

        sim.println("Outstring ready");

        try {
            fr.println(outString);
        } catch (Exception e) {
            sim.print("Error in printOutput");
        }

        sim.println("Printed");
    }

    /*
     * For an inputted angle of attack and sideslip, calculates the necessary flow
     * direction
     */
    public double[] calculateFlowAngle(double aoa, double beta) {
        double x = Math.sin(Math.toRadians(beta));
        double y = Math.sin(Math.toRadians(aoa)) * Math.cos(Math.toRadians(beta));
        double z = -Math.cos(Math.toRadians(aoa)) * Math.cos(Math.toRadians(beta));
        
        double[] toRet = {x,y,z};
        
        return toRet;        
    }
}