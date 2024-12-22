      * This program saves the high scores of our game
       IDENTIFICATION DIVISION.
       PROGRAM-ID. MOVETOHS.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
       SELECT TEMPFILE ASSIGN TO "records\temp.txt"
           ORGANIZATION IS LINE SEQUENTIAL.

       SELECT HIGHSCORESFILE ASSIGN TO "records\high_scores.txt"
           ORGANIZATION IS LINE SEQUENTIAL.

       DATA DIVISION.
       FILE SECTION.
       FD TEMPFILE.
       01 TEMPSCORE.
           88 ENDOFCS                    VALUE HIGH-VALUES.
           05 SCORE                      PIC 9(10).
       
       FD HIGHSCORESFILE.
       01 HIGHSCORELINE                PIC 9(10).

       WORKING-STORAGE SECTION.
       01 WS-CS.
           05 PLAYERSCORE                  PIC 9(10).
      
       PROCEDURE DIVISION.

       0050-OPEN-FILE.
           OPEN INPUT TEMPFILE.
           OPEN OUTPUT HIGHSCORESFILE.
           PERFORM 0100-PROCESS.
           PERFORM 0200-STOP-RUN. 
           
       0100-PROCESS.
            READ TEMPFILE
            AT END SET ENDOFCS TO TRUE
            END-READ.

            PERFORM UNTIL ENDOFCS
               MOVE SCORE TO WS-CS
               MOVE WS-CS TO HIGHSCORELINE
               WRITE HIGHSCORELINE
               READ TEMPFILE
               AT END SET ENDOFCS TO TRUE
               END-READ
            END-PERFORM.
       0200-STOP-RUN.
           CLOSE HIGHSCORESFILE.
           CLOSE TEMPFILE.
           STOP RUN.

       END PROGRAM MOVETOHS.
 