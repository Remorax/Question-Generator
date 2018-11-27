package edu.cmu.ark.ranking;

public class RankerFactory {
	public static IRanker createRanker(String type){
		IRanker res;
		
		//took out other options for simplicity
		res = new WekaLinearRegressionRanker();
			
		return res;
	}
}
