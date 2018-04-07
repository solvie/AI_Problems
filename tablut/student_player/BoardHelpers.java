package student_player;

import tablut.TablutBoardState;

public class BoardHelpers {
	public static boolean areBoardsEqual(TablutBoardState bs1, TablutBoardState bs2) {
		if (!bs1.getPlayerPieceCoordinates().equals(bs2.getPlayerPieceCoordinates())) return false;
		if (!bs1.getOpponentPieceCoordinates().equals(bs2.getOpponentPieceCoordinates())) return false;
		//bs1.printBoard();
		return true;
		
	}
}
