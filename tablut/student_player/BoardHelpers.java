package student_player;

import java.util.List;

import coordinates.Coord;
import coordinates.Coordinates;
import tablut.TablutBoardState;

public class BoardHelpers {
	public static boolean areBoardsEqual(TablutBoardState bs1, TablutBoardState bs2) {
		if (!bs1.getPlayerPieceCoordinates().equals(bs2.getPlayerPieceCoordinates())) return false;
		if (!bs1.getOpponentPieceCoordinates().equals(bs2.getOpponentPieceCoordinates())) return false;
		//bs1.printBoard();
		return true;
		
	}
	
    // Given a coordinate, returns the distance between it and the closest corner.
    public static Coord closestCorner(Coord kingPos) {
        List<Coord> corners = Coordinates.getCorners();
        int minDistance = Integer.MAX_VALUE;
        Coord closestCorner = corners.get(0);
        for (Coord corner : corners) {
            int distance = kingPos.distance(corner);
            if (distance < minDistance) {
                minDistance = distance;
                closestCorner = corner;
            }
        }
        return closestCorner;
    }
    
    public static boolean isPieceBetweenKingAndCorner(Coord piece, Coord king, Coord corner) {
    	boolean a,b;
    	if (piece.x == king.x) {//check if the y is in between
    		// if the distances are the same sign, it is in the way.
    		a = (corner.y - piece.y)>0;
    		b = (piece.y- king.y)>0; 
    		return !a^b;
    		
    	} else if (piece.y == king.y) {//check if x is in between
    		a = (corner.x - piece.x)>0;
    		b = (piece.x- king.x)>0;
    		return !a^b;
    	} else {
    		return false;
    	}
    
    }
    
    
}
