from django.db.models import Avg, Count, F, Max, Min, Prefetch, Q, Sum
from django.shortcuts import render
from django.views import View

from .models import Competition, Footballer, Team


class ComplexQuery(View):

    def get(self, request):
        annotate = []
        pc_team_list = []
        pr_competition_list = []

        F_expression = Footballer.objects.filter(season_assists__gt=F('season_goals'))
        Q_expression = Footballer.objects.filter(Q(age__lte=40), Q(season_goals__gt=10) | Q(season_assists__lte=20))
        Annotation = Footballer.objects.annotate(goal_contribution=(F('season_goals') + F('season_assists')))
        Aggregation = Footballer.objects.all().aggregate(total_season_goals = Sum('season_goals'))
        Average_goals = Footballer.objects.all().aggregate(averagel_season_goals = Avg('season_goals'))
        Minimum_goals = Footballer.objects.all().aggregate(minimum_season_goals = Min('season_goals'))
        Maximum_goals = Footballer.objects.all().aggregate(maximum_season_goals = Max('season_goals'))
        Count_goals = Footballer.objects.annotate(total_goals = Count('season_goals'))

        for footballer in Annotation:
            annotate.append(footballer.goal_contribution)

        # normal case ie, without use select or prefetch related:
        # footballer = Footballer.objects.all()
        # teams = [ft.team.name for ft in footballer]

        # # select related - get all teams of footballer   -for fk or onetoone
        footballer = Footballer.objects.select_related('team').all()
        sr_teams = [ft.team.name for ft in footballer]


        # prefetch_related - get competitions of a Footballer (Footballer by Footballer)  -for manytomany
        # footballer = Footballer.objects.all()    ## normal case ie, without use select or prefetch related:
        footballer = Footballer.objects.prefetch_related('competitions').all()
        for ft in footballer:
            competitions = ft.competitions.all()
            for competition in competitions:
                pr_competition_list.append(competition)

        # using Prefetch Class together with prefetch_related - get Footballer of all teams
        # teams = Team.objects.all()
        teams = Team.objects.all().prefetch_related(
            Prefetch('footballer_set',queryset=Footballer.objects.all())
        )
        for team in teams:
            footballer = team.footballer_set.all()
            for ft in footballer:
                pc_team_list.append(ft.name)

        context = {
            'F_expression': F_expression,
            'Q_expression': Q_expression,
            'annotate': annotate,
            'aggregation':Aggregation,
            'Average_goals':Average_goals,
            'Minimum_goals':Minimum_goals,
            'Maximum_goals':Maximum_goals,
            'Count_goals':Count_goals,

            'sr_teams':sr_teams,
            'pr_competition_list':pr_competition_list,
            'pc_team_list':pc_team_list

        }
        return render(request, 'complex-query.html', context)
