import typing
from enum import EnumType
from gettext import ngettext

import click
from click import Parameter, Context


class StringEnumChoice(click.Choice):
    def __init__(self, enum_type: EnumType, case_sensitive: bool = True) -> None:
        choices = [f"{value.value}" for value in enum_type]
        super().__init__(choices, case_sensitive)
        self._enum_type = enum_type

    def convert(
        self,
        value: typing.Any,
        param: typing.Optional[Parameter],
        ctx: typing.Optional[Context],
    ) -> typing.Any:
        try:
            return self._enum_type(str(value))
        except ValueError:
            choices_str = ", ".join(map(repr, self.choices))
            self.fail(
                ngettext(
                    "{value!r} is not {choice}.",
                    "{value!r} is not one of {choices}.",
                    len(self.choices),
                ).format(value=value, choice=choices_str, choices=choices_str),
                param,
                ctx,
            )
