package student_player;

import java.util.HashSet;
import java.util.List;
import java.util.Random;

import boardgame.Board;
import boardgame.Move;
import coordinates.*;
import tablut.TablutBoardState;
import tablut.TablutMove;
import tablut.TablutPlayer;

/** A player file submitted by a student. */
public class TimidlyGreedyPlayer extends TablutPlayer {
	
	private Random rand = new Random(194753); //arbitrary seed
	/**
     * You must modify this constructor to return your student number. This is
     * important, because this is what the code that runs the competition uses to
     * associate you with your agent. The constructor should do nothing else.
     */
    public TimidlyGreedyPlayer() {
        super("260577764");
    }

    /**
     * This is the primary method that you need to implement. The ``boardState``
     * object contains the current state of the game, which your agent must use to
     * make decisions.
     */
    public Move chooseMove(TablutBoardState boardState) {
    	return chooseTimidlyGreedyMove(boardState);
    }
    

    private TablutMove chooseTimidlyGreedyMove(TablutBoardState bs) { //adapted from GreedyTablutPlayer
    	List<TablutMove> options = bs.getAllLegalMoves();

        // Set an initial move as some random one.
        TablutMove bestMove = options.get(rand.nextInt(options.size()));

        // This greedy player seeks to capture as many opponents as possible.
        int opponent = bs.getOpponent();
        int minNumberOfOpponentPieces = bs.getNumberPlayerPieces(opponent);
        boolean moveCaptures = false;
        double evalFuncVal = 0;

        // Iterate over move options and evaluate them.
        for (TablutMove move : options) {
            // To evaluate a move, clone the boardState so that we can do modifications on it.
            TablutBoardState cloneBS = (TablutBoardState) bs.clone();

            // Process that move, as if we actually made it happen.
            cloneBS.processMove(move);

            // Check how many opponent pieces there are now, maybe we captured some!
            int newNumberOfOpponentPieces = cloneBS.getNumberPlayerPieces(opponent);
            
            /*
             * If we also want to check if the move would cause us to win, this works for
             * both! This will check if black can capture the king, and will also check if
             * white can move to a corner, since if either of these things happen then a
             * winner will be set.
             */
            if (cloneBS.getWinner() == player_id) {
                return move;
            }

            // If this move caused some capturing to happen, look one more step ahead and see if the opponent might capture as a result.
            if (newNumberOfOpponentPieces < minNumberOfOpponentPieces) {
            	//TODO
                bestMove = move;
                minNumberOfOpponentPieces = newNumberOfOpponentPieces;
                moveCaptures = true;
            }

            if (player_id == TablutBoardState.SWEDE) { //if we can advance the king WITHOUT dying from it, do it. 
            	TablutBoardState kingMovedBs = (TablutBoardState)bs.clone();
            	kingMovedBs.processMove(move);
            	double currentEval = computeEvaluationFunction(bs.getKingPosition(), kingMovedBs);
            	if (currentEval>evalFuncVal) {
            		evalFuncVal = currentEval;//update 
            		bestMove = move;
            	}
            }
        }
        return bestMove; 
    }
    
    //measures the goodness of a board state for a swede. Higher values is good.
    //if it puts the king in danger of being eaten, returns 0 immediately
    //if there's someone in the way of the king as a result of doing this, return 0
    private double computeEvaluationFunction(Coord prevKingPos, TablutBoardState bs) {
    	//is the king in danger of being eaten as a result of this move?
        List<TablutMove> potentialEnemyMoves = bs.getAllLegalMoves();

        for (TablutMove potentialEnemyMove : potentialEnemyMoves) {
            TablutBoardState cloned = (TablutBoardState) bs.clone();
        	cloned.processMove(potentialEnemyMove);
        	if (cloned.getWinner()==TablutBoardState.MUSCOVITE) {
        		return 0;
        	}
        }
        
    	Coord kingPos = bs.getKingPosition();

    	//is there someone in the king's direct line of movement, closer to that corner? If so don't make the move.
        HashSet<Coord> opponentCoords = bs.getOpponentPieceCoordinates();
        for (Coord opponentpiece : opponentCoords) {
        	if (BoardHelpers.isPieceBetweenKingAndCorner(opponentpiece, kingPos, BoardHelpers.closestCorner(kingPos)))
        		return 0;
        }
        
    	//Did the king get closer to the corner?
    	double kingCloserBy = 0;
        int minDistance = Coordinates.distanceToClosestCorner(kingPos);
        int prevDistance  =Coordinates.distanceToClosestCorner(prevKingPos);
        if (minDistance<prevDistance) {
        	kingCloserBy = prevDistance-minDistance;
        }
        return kingCloserBy;
    }
    
    
}