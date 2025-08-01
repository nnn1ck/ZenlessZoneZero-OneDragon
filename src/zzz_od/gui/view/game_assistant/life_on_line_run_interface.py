from PySide6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon
from typing import Optional

from one_dragon.base.config.config_item import ConfigItem
from one_dragon.base.operation.application_base import Application
from one_dragon_qt.widgets.setting_card.combo_box_setting_card import ComboBoxSettingCard
from one_dragon_qt.widgets.setting_card.help_card import HelpCard
from one_dragon_qt.widgets.setting_card.spin_box_setting_card import SpinBoxSettingCard
from one_dragon_qt.view.app_run_interface import AppRunInterface
from zzz_od.application.life_on_line.life_on_line_app import LifeOnLineApp
from zzz_od.application.zzz_application import ZApplication
from zzz_od.context.zzz_context import ZContext

from one_dragon_qt.widgets.column import Column

class LifeOnLineRunInterface(AppRunInterface):

    def __init__(self,
                 ctx: ZContext,
                 parent=None):
        self.ctx: ZContext = ctx
        self.app: Optional[ZApplication] = None

        AppRunInterface.__init__(
            self,
            ctx=ctx,
            object_name='life_on_line_run_interface',
            nav_text_cn='拿命验收',
            parent=parent,
        )

    def get_widget_at_top(self) -> QWidget:
        content = Column()

        self.help_opt = HelpCard(url='https://one-dragon.com/zzz/zh/docs/feat_game_assistant.html#_2-%E6%8B%BF%E5%91%BD%E9%AA%8C%E6%94%B6')
        content.add_widget(self.help_opt)

        self.daily_plan_times_opt = SpinBoxSettingCard(icon=FluentIcon.CALENDAR, title='每日次数')
        content.add_widget(self.daily_plan_times_opt)

        self.team_opt = ComboBoxSettingCard(
            icon=FluentIcon.PEOPLE,
            title='预备编队',
        )
        content.add_widget(self.team_opt)

        return content

    def on_interface_shown(self) -> None:
        AppRunInterface.on_interface_shown(self)

        self.daily_plan_times_opt.init_with_adapter(self.ctx.life_on_line_config.get_prop_adapter('daily_plan_times'))
        self.daily_plan_times_opt.setContent('完成次数 当日: %d' % self.ctx.life_on_line_record.daily_run_times)

        config_list = ([ConfigItem('游戏内配队', -1)] +
                       [ConfigItem(team.name, team.idx) for team in self.ctx.team_config.team_list])
        self.team_opt.set_options_by_list(config_list)
        self.team_opt.init_with_adapter(self.ctx.life_on_line_config.predefined_team_idx_adapter)

    def get_app(self) -> Application:
        return LifeOnLineApp(self.ctx)
