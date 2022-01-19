import urwid

def __init__(self, project):
    self.project = project

    self.notifier = generic.FooterNotifier("")

    self.tabs = generic.Tabs(self.TABS)

    # Subviews
    self.backlog = ProjectBacklogSubView(self, project, self.notifier, self.tabs)
    self.sprint = ProjectMilestoneSubView(self, project, self.notifier, self.tabs)
    self.issues = ProjectIssuesSubView(self, project, self.notifier, self.tabs)
    self.wiki = ProjectWikiSubView(self, project, self.notifier, self.tabs)
    self.admin = ProjectAdminSubView(self, project, self.notifier, self.tabs)

    self.widget = urwid.Frame(self.backlog.widget,
                              header=projects.ProjectDetailHeader(project),
                              footer=generic.Footer(self.notifier))