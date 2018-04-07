package student_player;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;


import boardgame.Board;
import boardgame.Move;
import tablut.TablutBoardState;
import tablut.TablutMove;
import tablut.TablutPlayer;

public class MontePlayer extends TablutPlayer
{
	private Random rand = new Random(194753); //arbitrary seed

	public MontePlayer() {
			
	}
	
	@Override
	public Move chooseMove(TablutBoardState boardState) {
		long startTime = System.currentTimeMillis();
    	long currentTime = startTime;
    	
        // You probably will make separate functions in MyTools.
		List<TablutMove> options = boardState.getAllLegalMoves();
		int numOptions = options.size();
		List<Double> numWins = new ArrayList<Double>(Collections.nCopies(numOptions, 0.0));

		TablutMove currentBestMove = options.get(rand.nextInt(options.size()));
		//double currentBestMoveNumWins = 0;//initialize the win statistic to 0.
		int iteration = 0; //starts at 0.
		double currentmaxval = 0;
		int currentbestmoveindex = 0;
        // For example, maybe you'll need to load some pre-processed best opening
        // strategies...
        //MyTools.getSomething();
		while (currentTime-startTime< 5950) { // 2 seconds is the limit
			iteration++;
			for (int i = 0; i<numOptions; i++) { //keep track of indices
				TablutBoardState clonedBS = (TablutBoardState) boardState.clone();
				clonedBS.processMove(options.get(i));
				int currentWinner = clonedBS.getWinner();
				while (currentWinner== Board.NOBODY) {
					List<TablutMove> moves = clonedBS.getAllLegalMoves();
					if (moves.size()==0) break;
					else
						clonedBS.processMove(moves.get(rand.nextInt(moves.size())));
				}
				currentWinner = clonedBS.getWinner();
				if (currentWinner== player_id) {
					numWins.set(i, numWins.get(i)+1);
				} //else if (currentWinner == Board.DRAW) {
				//	numWins.set(i, numWins.get(i)+0.5);
				//}
				if (numWins.get(i)>currentmaxval) {
					currentbestmoveindex = i;
					currentmaxval = numWins.get(i);
				}
			}
			currentTime = System.currentTimeMillis();
			long diff = currentTime-startTime;
			System.out.println("current time elapsed is: "+ diff);

		}
		currentBestMove = options.get(currentbestmoveindex);
		
		System.out.println("current iterations is: "+ iteration );
        // Return your move to be processed by the server.
        return currentBestMove;
	}

}
