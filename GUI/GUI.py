from src.TicTacToe import TicTacToe
from src.Agent import Agent
import wx
import wx.lib.newevent
import wx.lib.mixins.inspection
import time


class TTTFrame(wx.Frame):
    GameOverEvent, EVT_GAME_OVER = wx.lib.newevent.NewEvent()

    def __init__(self):
        """Initialize the backend, menus, main grid and GameOver event."""
        wx.Frame.__init__(self, parent=None, title='Tic-Tac-Toe', size=wx.Size(475, 525))

        self.CreateMenus()
        self.CreateStatusBar(number=1, style=wx.STB_DEFAULT_STYLE, id=-1)

        self.Bind(self.EVT_GAME_OVER, handler=self.OnGameOver)

    def CreateMenus(self):
        """Create all the menus."""
        fileMenu = wx.Menu()

        newMenuItem = fileMenu.Append(wx.ID_NEW,
                                      item='&New Game',
                                      helpString="Create a new game")
        self.Bind(event=wx.EVT_MENU, handler=self.OnNewGame, source=newMenuItem)
        fileMenu.AppendSeparator()
        abtMenuItem = fileMenu.Append(wx.ID_ABOUT,
                                      item='&About',
                                      helpString="Information about this Tic-Tac-Toe game")
        self.Bind(event=wx.EVT_MENU, handler=self.OnAbout, source=abtMenuItem)
        exitMenuItem = fileMenu.Append(wx.ID_EXIT,
                                       item='&Exit',
                                       helpString="Terminate the Tic-Tac-Toe program")
        self.Bind(event=wx.EVT_MENU, handler=self.OnExit, source=exitMenuItem)

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')  # Adding the "fileMenu" to the MenuBar

        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame object.

    def PromptForToken(self):
        """Prompt user for their choice of X or O, return True if they choose X, False if O."""
        dlg = wx.MessageDialog(self,
                               "",
                               caption="X/O?",
                               style=wx.YES_NO | wx.CANCEL)
        if dlg.SetYesNoLabels("&X", "&O"):
            dlg.SetMessage("Do you want to play with the 'X's or with the 'O's?")
        else:  # Cannot change values of buttons: they have std YES/NO value so rephrase question.
            dlg.SetMessage("Would you prefer to play with the 'X's this time?")
        return dlg.ShowModal()

    def ClearMainGrid(self):
        """Reset the main grid and the status bar."""
        for btn in self.mainGrid.buttons:
            btn.SetBitmap(self.mainGrid.img_blank)
            btn.Enable()
            self.SetStatusText('Welcome to Tic-Tac-Toe!')
        self.Refresh()

    def DisableGrid(self):
        """Disable all buttons on the grid."""
        for btn in self.mainGrid.buttons:
            btn.Disable()

    def EnableGrid(self):
        """Enables all unused buttons on the grid."""
        for btn in self.mainGrid.buttons:
            if self.board.valid_move(btn.GetId()):
                btn.Enable()

    def DoMove(self, pos):
        """Update backend state and button labels after a move is played."""
        cur_player = self.board.current_player()
        self.board.move(pos)
        btn = self.mainGrid.buttons[pos]
        btn.SetBitmap(
            {'X': self.mainGrid.img_x, 'O': self.mainGrid.img_o}[cur_player]
        )
        btn.SetBitmapDisabled(
            {'X': self.mainGrid.img_x, 'O': self.mainGrid.img_o}[cur_player]
        )
        self.Refresh()

    def AgentMove(self):
        """Choose and play next move for AI."""
        self.SetStatusText(f"{self.board.current_player()} to move!")
        pos = self.agent.choose_move(self.board)
        self.DoMove(pos)
        if self.board.over():
            evt = self.GameOverEvent()
            wx.PostEvent(self, evt)

    def GameOver(self):
        """
        Triggers GameOverEvent if the game is over.

        Return False if game is not over yet.
        """
        if self.board.over():
            evt = self.GameOverEvent()
            wx.PostEvent(self, evt)
            return True
        else:
            return False

    def OnNewGame(self, event):
        """Creates a new game."""
        playerTokenAnswer = self.PromptForToken()  # Prompts user for his choice of token X or O.
        if playerTokenAnswer == wx.ID_CANCEL:  # Do nothing if user cancelled the NewGame..
            return
        if not hasattr(self, 'board'):
            self.board = TicTacToe()
            self.agent = Agent()
            self.mainGrid = TTTPanel(self)
            self.Layout()
        else:
            self.ClearMainGrid()
            self.board.clear()
        self.over = False
        if playerTokenAnswer == wx.ID_YES:  # Player chose 'X'.
            self.agent.token = 'O'
            self.SetStatusText("X to start!")
        else:  # Player chose 'O'.
            self.agent.token = 'X'
            self.SetStatusText("Computer is thinking...")
            self.AgentMove()
            self.SetStatusText("O to move!")

    def OnAbout(self, event):
        """A simple dialogue box with an OK button."""
        message = "This small program implements the minimax algorithm to provide an opponent " \
                  "that will play perfectly and never lose.\nEverything is written in Python, " \
                  "and the GUI is built using the wxPython library."
        wx.MessageBox(message, caption="About", style=wx.OK, parent=self)

    def OnExit(self, event):
        dlg = wx.MessageDialog(self,
                               "Are you sure you want to exit?",
                               caption="(Y/c)?",
                               style=wx.YES_NO)
        dlg.SetYesNoLabels(wx.ID_YES, wx.ID_CANCEL)
        answer = dlg.ShowModal()
        if answer == wx.ID_YES:
            self.Close(True)

    def OnButton(self, event):
        """Handle the buttons getting pressed."""
        self.DisableGrid()
        pos = event.GetId()
        if self.board.valid_move(pos):
            self.DoMove(pos)
            if self.GameOver():  # The GameOver event is triggered inside this function call.
                pass
            else:
                time.sleep(0.2)
                self.AgentMove()
        else:
            self.SetStatusText(f"Invalid choice, {self.board.current_player()} to move!")
        self.EnableGrid()

    def OnGameOver(self, event):
        """Handle the game being over."""
        self.over = True
        self.DisableGrid()
        if self.board.drawn():
            self.SetStatusText("Game is drawn!")
        else:
            self.SetStatusText(f"Game over, {self.board.winner()} wins!")


class TTTPanel(wx.Panel):
    """The Panel holding the main grid consisting of 9 buttons."""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.CreateMainGrid()

    def CreateMainGrid(self):
        """Create the main grid used to display state and receive user moves."""
        self.img_blank = wx.Bitmap("blank.png", type=wx.BITMAP_TYPE_PNG)
        self.img_blank.SetSize(wx.Size(150, 150))
        self.img_x = wx.Bitmap("X_token.png", type=wx.BITMAP_TYPE_PNG)
        self.img_x.SetSize(wx.Size(150, 150))
        self.img_o = wx.Bitmap("O_token.png", type=wx.BITMAP_TYPE_PNG)
        self.img_o.SetSize(wx.Size(150, 150))

        gs = wx.GridSizer(3, gap=wx.Size(0, 0))
        self.buttons = []

        for i in range(9):
            self.buttons.append(wx.Button(self,
                                id=i,
                                label="",
                                style=wx.BU_EXACTFIT | wx.BU_NOTEXT | wx.BORDER_NONE))
            gs.Add(self.buttons[i], proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
            self.Bind(wx.EVT_BUTTON,
                      handler=self.GetParent().OnButton,
                      source=self.buttons[i])
            self.buttons[i].SetBitmap(self.img_blank)
            self.buttons[i].SetBitmapDisabled(self.img_blank)

        self.SetAutoLayout(True)
        self.SetSizerAndFit(gs)


class MyApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        self.Init()
        frame = TTTFrame()
        frame.Show()
        self.SetTopWindow(frame)

        return True


if __name__ == '__main__':
    app = MyApp(redirect=False)
    app.MainLoop()
