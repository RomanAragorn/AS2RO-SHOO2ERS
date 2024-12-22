      * This program saves the high scores of our game
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HIGHSCORE.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
       SELECT CURRENTSCOREFILE ASSIGN TO "records\high_scores.txt"
           ORGANIZATION IS LINE SEQUENTIAL.

       SELECT TEMPFILE ASSIGN TO "records\temp.txt"
           ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD CURRENTSCOREFILE.
       01 CURRENTSCORE.
           05 SCORE                      PIC 9(10).
       
       FD TEMPFILE.
       01 TEMPLINE                PIC 9(10).

       WORKING-STORAGE SECTION.
       01 WS-CS.
           05 PLAYERSCORE                  PIC 9(10).
       
       01 WS-TEMP.
           05 WS-HS                     PIC 9(10).
       
       01  WS-COUNT                        PIC 9 VALUE 0.
       01  WS-PH                          PIC 9 VALUE 0.
       01  ENDOFCS                        PIC 9 VALUE 0.

       
       01 J    PIC 9(10)                  VALUE 1.
       01 K    PIC 9(10)                  VALUE 1.
       01 I1   PIC 9(10)                  VALUE 1.
       01 TMP  PIC 9(10)                 VALUE 1.
       01 CR   PIC X(2).
       01 ARR1.
           03 ARR PIC 9(10) OCCURS 10 TIMES INDEXED BY I.
       PROCEDURE DIVISION.

       0050-OPEN-FILE.
           OPEN INPUT CURRENTSCOREFILE.
           OPEN OUTPUT TEMPFILE.
           PERFORM 0100-PROCESS.
           PERFORM 0200-STOP-RUN. 
           
       0100-PROCESS.
           PERFORM UNTIL I > 9
               IF ENDOFCS IS EQUAL TO 0 THEN
                  PERFORM UNTIL ENDOFCS EQUALS 1
                       READ CURRENTSCOREFILE
                       AT END
                          MOVE 1 TO ENDOFCS
                       END-READ
                       MOVE CURRENTSCORE TO WS-CS 
                       MOVE WS-CS TO ARR(I)
                       ADD 1 TO I
                  END-PERFORM
               
               ELSE
                  MOVE 0000000000 TO WS-CS
                  MOVE WS-CS TO ARR(I)
                  ADD 1 TO I
               END-IF
           END-PERFORM.
           
           PERFORM UNTIL J > 9
               MOVE 1 TO I
               PERFORM UNTIL I > 8 
                   ADD 1 TO I GIVING I1
                   IF ARR(I) <= ARR(I1) THEN
                       MOVE ARR(I) TO TMP
                       MOVE ARR(I1) TO ARR(I)
                       MOVE TMP TO ARR(I1)
                   END-IF
                   ADD 1 TO I
               END-PERFORM
               MOVE 1 TO K
               PERFORM UNTIL K > 9
                   DISPLAY ARR(K) WITH NO ADVANCING 
                   DISPLAY ", " WITH NO ADVANCING
                   ADD 1 TO K
               END-PERFORM
               DISPLAY "  "
               ADD 1 TO J
           END-PERFORM.
           MOVE 1 TO I.
           PERFORM UNTIL I > 9
               MOVE ARR(I) TO TEMPLINE
               WRITE TEMPLINE
               ADD 1 TO I
           END-PERFORM.

       0200-STOP-RUN.
           CLOSE CURRENTSCOREFILE.
           CLOSE TEMPFILE.
           STOP RUN.

       END PROGRAM HIGHSCORE.
 