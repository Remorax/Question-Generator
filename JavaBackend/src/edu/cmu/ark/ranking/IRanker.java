package edu.cmu.ark.ranking;

import java.util.*;

public interface IRanker{
	public void train(List<List<Rankable>> trainData);
	
	public void rank(List<Rankable> unranked);
	public void rankAll(Collection<List<Rankable>> unrankedCollections);

	public void setParameter(String key, Double value);
	public Double getParameter(String key);
	
	public void rank(List<Rankable> unranked, boolean doSort);
	public void rankAll(Collection<List<Rankable>> testData, boolean doSort);
	
}
