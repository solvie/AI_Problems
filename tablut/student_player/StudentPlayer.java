package student_player;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Random;
import java.util.Timer;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import boardgame.Board;
import boardgame.Move;
import coordinates.*;
import tablut.TablutBoardState;
import tablut.TablutMove;
import tablut.TablutPlayer;

/** A player file submitted by a student. */
public class StudentPlayer extends TablutPlayer {
	TreeNode treeRoot;
	TreeNode prevNode; 
	
	private Random rand = new Random(194753); //arbitrary seed
	//ExecutorService service = Executors.newSingleThreadExecutor();
    /**
     * You must modify this constructor to return your student number. This is
     * important, because this is what the code that runs the competition uses to
     * associate you with your agent. The constructor should do nothing else.
     */
    public StudentPlayer() {
        super("260577764");
    }

    /**
     * This is the primary method that you need to implement. The ``boardState``
     * object contains the current state of the game, which your agent must use to
     * make decisions.
     */
    public Move chooseMove(TablutBoardState boardState) {
    	if (boardState.getTurnNumber()<1) {
    		return mcts(boardState, true);
    	}else {
    		TablutMove move = mcts(boardState, false);
    		return move;
    	}
    }
    
    /**
     * follow the tree down to after the enemy plays, return the result.
     * 
     * @return
     */
    private TreeNode traceEnemyPath(TreeNode startNode, TablutBoardState currentBoardState) {
		List<TreeNode> enemyMovePossibilities = startNode.getChildren(); //from current root.
		if (enemyMovePossibilities.size()>0) {
			//System.out.println("\n\n Enemy moves that led to this point coulda been "+enemyMovePossibilities.size());
			//System.out.println("tree root chilren size is: "+treeRoot.getNumChildren());
			for (TreeNode enemyMoveResult: enemyMovePossibilities) {
    			//System.out.println("candidate IS:");
    			//enemyMoveCand.getBoardState().printBoard();
    			//System.out.println("COMPARE me to now");
    			if (BoardHelpers.areBoardsEqual(enemyMoveResult.getBoardState(), currentBoardState))
    				return enemyMoveResult;
    		}
		}
    	return null;
    }
    
    private TreeNode doSelection(TreeNode root) {
    	TreeNode retVal = root; //initialize as root
		while(true) { //while we haven't reached a leaf
			if (retVal.isLeaf()) break;
			TreeNode selectedChild = retVal.selectChildWithBestQ();
			retVal = selectedChild;
		}
		return retVal;
    }
    
    public TablutMove mcts(TablutBoardState boardState, boolean initialize) { //This is for our 30 second initialization
    	long timeoutval;
		long startTime ;
    	long currentTime ;
    	if (initialize) {
    		timeoutval = 10000; //short for test (AND BECAUSE OF MEMORY)
    		treeRoot = new TreeNode(null, null, boardState);
    		startTime = System.currentTimeMillis();
    		currentTime = startTime;
    	} else {  
    		startTime = System.nanoTime();
    		currentTime = startTime;
    		timeoutval = 1000000000; //short for test
    		TreeNode rootAfterEnemyMove = traceEnemyPath(treeRoot, boardState);
    		if (rootAfterEnemyMove!=null) {
    			treeRoot = rootAfterEnemyMove;
    		} else {
    			System.out.println("\n\n THIS AINT GREAT, enemy move didn't exist, we're gonna have to start over");
        		treeRoot = new TreeNode(null, null, boardState);
    		}
    		
    	}

		 //currentNode = treeRoot;
 
    	while (currentTime - startTime<timeoutval) {
    		//1. SELECTION
    		TreeNode currentNode = doSelection(treeRoot);
//			System.out.println(System.nanoTime() - startTime);
//			System.out.println("time after select");
    		//2. EXPANSION, PLAYOUT, BACKPROP
			TablutBoardState clonedboardstate = currentNode.cloneBoardState();

    		if (!currentNode.playedOut()) {
//    			System.out.println(System.nanoTime() - startTime);
//    			System.out.println("time before playout");
    			boolean timeoutWarning= false;
    			// If it hasn't been played out yet, play it out
    			
    			while (clonedboardstate.getWinner()==Board.NOBODY) { //greedily
    	    		if(initialize)
    	    	    	currentTime = System.currentTimeMillis();
    	        		else currentTime = System.nanoTime();
    				if (currentTime - startTime>timeoutval) {
//    	    			System.out.println(System.nanoTime() - startTime);
    					System.out.println("TIMEOUT WARNING");
    					timeoutWarning = true;
    					break;
    				}
    				TablutMove move = chooseRandomMove(clonedboardstate);
//	    			System.out.println(System.nanoTime() - startTime);
//					System.out.println("time after choosing random move");
    				
    				//TablutMove move = chooseRandomMoveWithSuddenDeath(clonedboardstate);
    	    		clonedboardstate.processMove(move);
//	    			System.out.println(System.nanoTime() - startTime);
//					System.out.println("time after processing move");
        			//System.out.println(System.nanoTime() - startTime);
        			//System.out.println("time after processing one move");
    	    		//clonedboardstate.processMove(chooseGreedyMove(clonedboardstate));
    			}
    			if (timeoutWarning) break;
//    			System.out.println(System.nanoTime() - startTime);
//    			System.out.println("time after playout");
    			
    			// Backprop the result.
//    			System.out.println(System.nanoTime() - startTime);
//    			System.out.println("time before backprop ");
    			currentNode.backProp(clonedboardstate.getWinner()==player_id);
//    			System.out.println(System.nanoTime() - startTime);
//    			System.out.println("time after backprop");
    			
    		} else {// if it has already been played out once, expand its children. 
    			//expand children
//    			System.out.println(System.nanoTime() - startTime);
//    			System.out.println("time before expanding children");
    			List<TablutMove> movesToGenerateChildrenFrom = clonedboardstate.getAllLegalMoves();
    			currentNode.setNumChildren(movesToGenerateChildrenFrom.size());
    			
    			//add all the children. don't play them out yet. 
    			for (TablutMove move: movesToGenerateChildrenFrom) {
    				TablutBoardState playedstate = currentNode.cloneBoardState();
    				playedstate.processMove(move);
    				currentNode.addChild(playedstate, move);
    			}
//    			System.out.println(System.nanoTime() - startTime);
//    			System.out.println("time after expanding children");
    		}
    		if(initialize)
	    	currentTime = System.currentTimeMillis();
    		else currentTime = System.nanoTime();
    	}
    	
    	//System.out.println("Currently board looks like this, before we make our move");
    	treeRoot.getBoardState().printBoard();
//		System.out.println(System.nanoTime() - startTime);
//		System.out.println("selecting child with best q");

		TreeNode chosenNode;
		TreeNode winner = treeRoot.selectWinningChild(player_id);
		if (winner!=null) chosenNode = winner;
		else chosenNode= treeRoot.selectChildWithBestQ();
		//chosenNode.getBoardState().printBoard();
		//System.out.println("WE WANT TO MOVE"+chosenNode.getParentMove().toPrettyString());
		//System.out.println("current time on record "+ currentTime);
		//System.out.println("actual current time " + System.currentTimeMillis());
		treeRoot = chosenNode;
		//System.out.println("PRINTING TREE");
		//treeRoot.printTree();
		System.out.println(treeRoot.nodeToString());
		System.out.println(currentTime - startTime);
		return chosenNode.getParentMove();

    }
    
    private TablutMove chooseRandomMove(TablutBoardState bs) {
    	List<TablutMove> options = bs.getAllLegalMoves();
    	return options.get(rand.nextInt(options.size()));
    }

    private TablutMove chooseRandomMoveWithSuddenDeath(TablutBoardState bs) {
    	List<TablutMove> options = bs.getAllLegalMoves();
    	for (TablutMove move : options) {
            TablutBoardState cloneBS = (TablutBoardState) bs.clone();
            // Process that move, as if we actually made it happen.
            cloneBS.processMove(move);
            // If this move caused some capturing to happen, then do it! Greedy!
            if (cloneBS.getWinner()==player_id) {
            	return move;
            }
        }
    	return options.get(rand.nextInt(options.size()));
    }
    
    private TablutMove chooseGreedyMove(TablutBoardState bs) {//todo: don't clone?
        List<TablutMove> options = bs.getAllLegalMoves();

        // Set an initial move as some random one.
        TablutMove bestMove = options.get(rand.nextInt(options.size()));

        // This greedy player seeks to capture as many opponents as possible.
        int opponent = bs.getOpponent();
        int minNumberOfOpponentPieces = bs.getNumberPlayerPieces(opponent);
        boolean moveCaptures = false;

        // Iterate over move options and evaluate them.
        for (TablutMove move : options) {
        	//System.out.println("looking at options...");
            // To evaluate a move, clone the boardState so that we can do modifications on
            // it.
            TablutBoardState cloneBS = (TablutBoardState) bs.clone();

            // Process that move, as if we actually made it happen.
            cloneBS.processMove(move);

            // Check how many opponent pieces there are now, maybe we captured some!
            int newNumberOfOpponentPieces = cloneBS.getNumberPlayerPieces(opponent);

            // If this move caused some capturing to happen, then do it! Greedy!
            if (newNumberOfOpponentPieces < minNumberOfOpponentPieces) {
            	//System.out.println("lets be greedy!");
                bestMove = move;
                minNumberOfOpponentPieces = newNumberOfOpponentPieces;
                moveCaptures = true;
            }

            /*
             * If we also want to check if the move would cause us to win, this works for
             * both! This will check if black can capture the king, and will also check if
             * white can move to a corner, since if either of these things happen then a
             * winner will be set.
             */
            if (cloneBS.getWinner() == player_id) {
                bestMove = move;
                moveCaptures = true;
                break;
            }
        }

        /*
         * The king-functionality below could be included in the above loop to improve
         * efficiency. But, this is written separately for the purpose of exposition to
         * students.
         */

        // If we are SWEDES we also want to check if we can get closer to the closest
        // corner. Greedy!
        // But let's say we'll only do this if we CANNOT do a capture.
        if (player_id == TablutBoardState.SWEDE && !moveCaptures) {
            Coord kingPos = bs.getKingPosition();
            
            //System.out.println("Whats king pos here theres a null bug :");
           // bs.printBoard();
            //System.out.println(kingPos);
            // Don't do a move if it wouldn't get us closer than our current position.
            int minDistance = Coordinates.distanceToClosestCorner(kingPos);

            // Iterate over moves from a specific position, the king's position!
            for (TablutMove move : bs.getLegalMovesForPosition(kingPos)) {
                /*
                 * Here it is not necessary to actually process the move on a copied boardState.
                 * Note that it is more efficient NOT to copy the boardState. Consider this
                 * during implementation...
                 */
                int moveDistance = Coordinates.distanceToClosestCorner(move.getEndPosition());
                if (moveDistance < minDistance) {
                    minDistance = moveDistance;
                    bestMove = move;
                }
            }
        }
        return bestMove; 
        }
    
    
    
}