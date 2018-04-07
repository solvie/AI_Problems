package student_player;

import java.util.ArrayList;
import java.util.List;

import tablut.TablutBoardState;
import tablut.TablutMove;

public class TreeNode {
	public static final double inf = Float.MAX_VALUE;
	private TablutBoardState boardstate;
	private TablutMove parentMove;
	private TreeNode parent;
	private List<TreeNode> children;
	private double numWins;
	private double numActionsTaken;
	private double Q;
	private int numChildren; //this is precautionary, not sure if will have to come into play
	
	public TreeNode(TreeNode parent, TablutMove parentMove ,TablutBoardState boardstate) {
		this.parent = parent;
		this.parentMove = parentMove;
		this.boardstate = (TablutBoardState) boardstate.clone();//TODO: does this have to be cloned?
		this.children = new ArrayList<TreeNode>();
		this.numWins = 0;
		this.numActionsTaken = 0;
		this.Q = inf;
	}
	
	private void updateQ(){
		if (this.numActionsTaken ==0) this.Q =inf;
		else { 
			double firstterm = numWins/numActionsTaken;
			//System.out.println("firstterm"+firstterm);

			double secondterm  = Math.sqrt(2*Math.log(this.parent.numActionsTaken)/numActionsTaken);
			//System.out.println("SECONDTERM"+secondterm);
			this.Q = firstterm+secondterm;
		}
	}
	
	public double getQ() {
		return this.Q;
	}
	
	public boolean playedOut() {
		if (numActionsTaken==0) return false;
		else return true;
	}
	
	public void backProp(boolean win) {
		//System.out.println("SECONDTERM"+secondterm);
		if (win) numWins++;
		numActionsTaken++;
		if (parent!=null) {
			updateQ();
			parent.backProp(win);
		}
	}
	
	
	public boolean isLeaf() {
		if (this.children.size()==0) return true;
		return false;
	}
	
	/**
	 * 
	 * @returns the one with the highest Q value, OR as soon as it finds one with inf.
	 */
	public TreeNode selectChildWithBestQ() {
		double currentBestVal = 0;
		TreeNode currentBestChild = null;
		for (TreeNode child: children) {
			double childsQ = child.getQ();
			if (childsQ== inf) return child;
			else if (childsQ>currentBestVal) {
				currentBestVal = childsQ;
				currentBestChild = child;
			}
		}
		return currentBestChild;
	}
	
	public TablutBoardState cloneBoardState() {
		return (TablutBoardState) this.boardstate.clone();
	}
	
	public void setNumChildren(int numChildren) {
		this.numChildren = numChildren;
	}
	
	public void addChild(TablutBoardState bs, TablutMove parentMove) {
		TreeNode child = new TreeNode(this, parentMove, (TablutBoardState)bs.clone());
		this.children.add(child);
	}
	
	public List<TreeNode> getChildren() {
		return this.children;
	}
	
	public TreeNode getParent() {
		return this.parent;
	}
	public TablutMove getParentMove() {
		return this.parentMove;
	}
	
	public TablutBoardState getBoardState() {
		return this.boardstate;
	}
	
	public int getNumChildren() {
		return this.numChildren;
	}
}
