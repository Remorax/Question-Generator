package edu.cmu.ark.ranking;

import java.text.NumberFormat;

public class Rankable implements Comparable<Object>{
	public String id;
	public double label;
	public double [] features;
	public double score;
	public Object pointer1; //e.g., to a question
	public Object pointer2;
	public Object pointer3; 
	
	public int compareTo(Object o) {
		return Double.compare(this.score, ((Rankable)o).score);
	}
	
	public String toString(){
		String res = "id="+id
			+"\tlabel="+NumberFormat.getInstance().format(label)
			+"\tscore="+NumberFormat.getInstance().format(score);
		if(features != null){
			for(int i=0;i<features.length;i++){
				res+="\t"+features[i];
			}
		}
		return res;
	}
}
