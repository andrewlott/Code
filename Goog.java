import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Goog {

	/**
	 * @param args
	 */
	public static void main(String[] args) {

		System.out.println("Input the Question File Name:");	//request input
		Scanner sc = new Scanner(System.in);					//make new Scanner
		String s = sc.next();									//get file name/path
		File file = new File("/Users/andrewlott/Documents/workspace/My Projects/src/" + s);	//create File object
		try {													//fuck this shit
			sc = new Scanner(file);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		String num_inputs = sc.nextLine();					//store number of inputs
		
		String [] all = new String [Integer.parseInt(num_inputs)];	//all outputs
		
		for(int i = 0; i < all.length; i++) {
			
			all[i] = in(sc.next(),sc.next(),sc.next());		//do it all!
			
		}
		
		for(int i = 0; i < all.length; i++)
			System.out.println("Case #" + (i+1) + ": " + all[i]);	//print it all!
		
	}
	
	public static String in(String number, String inlang, String outLang) {

		int num = 0;
					
		for(int i = 0; i < number.length(); i++) {
			
			num += java.lang.Math.pow(inlang.length(), number.length()-i-1)*inlang.indexOf(number.charAt(i));	//MATH IS POWER
					
		}		
		
		return toOutput(num, outLang);	//GET OUTTA HERE
	}
	
	public static String toOutput(int number, String lang) {
	
		String s = "";
		while( number > 0 ) {
			s += lang.charAt(number % lang.length());		//MATHS
			number /= lang.length();
			
		}		
		
		return new StringBuffer(s).reverse().toString();	//"I PUT MY THING DOWN, FLIP IT, AND REVERSE IT" (http://www.azlyrics.com/lyrics/missymisdemeanorelliott/workit.html)
	}
}

