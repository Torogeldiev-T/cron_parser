# import regular expression library
import re
from enum import Enum


class Controller(Enum):
    MINUTES = 61
    HOURS = 25
    DAYS_OF_MONTH = 32
    MONTHS = 13
    DAYS_OF_WEEK = 8


class Cron:
    # defines necessery fields of the class
    # lists which hold resulted values
    minutes = []
    hours = []
    days_month = []
    months = []
    days_week = []

    # constructor
    def __init__(self, arg):
        # splits given argument into tokens by " " delimeter
        self.tokens = arg.split(" ")
        if len(self.tokens) != 6:
            raise RuntimeError(
                "Number of arguments should be equal to 6: <current_number> <hour> <day(month)> <month> <days(week)> <path to file>"
            )
        # sets the path to the command
        self.command = self.tokens[5]

    # parses the given argument
    def parse(self):

        # uses a regex to find all numbers in the tokens to use them later
        minute_digits = re.findall("[0-9]+", self.tokens[0])
        hours_digits = re.findall("[0-9]+", self.tokens[1])
        days_month_digits = re.findall("[0-9]+", self.tokens[2])
        month_digits = re.findall("[0-9]+", self.tokens[3])
        days_week_digits = re.findall("[0-9]+", self.tokens[4])

        # validate the expression for minutes
        self.validate_minutes(minute_digits, self.tokens[0])
        # validate the expression for hours
        self.validate_hours(hours_digits, self.tokens[0])
        # validate the expression for days of month
        self.validate_days_of_month(days_month_digits, self.tokens[0])
        # validate the expression for months
        self.validate_months(month_digits, self.tokens[0])
        # validate the expression for days of week
        self.validate_days_of_week(days_week_digits, self.tokens[0])

        # parses the token for the minutes
        self.minutes = self.parse_current(0, self.tokens[0], [], 0, minute_digits, 60)
        # parses the token for the hours
        self.hours = self.parse_current(0, self.tokens[1], [], 0, hours_digits, 24)
        # parses the token for the days of month
        self.days_month = self.parse_current(
            0, self.tokens[2], [], 0, days_month_digits, 32
        )
        # parses the token for the months
        self.months = self.parse_current(0, self.tokens[3], [], 0, month_digits, 13)
        # parses the token for the days of week
        self.days_week = self.parse_current(
            0, self.tokens[4], [], 0, days_week_digits, 8
        )
        self.finalize()

    # recursively called method to return results for the given controller (minutes or hours or...days of week)
    def parse_current(
        self, idx, token, current_res, controller_idx, controller_digits, controller
    ):
        # get current <controller> number if there are any digits in token
        if len(controller_digits) > 0:
            current_number = controller_digits[controller_idx]

        # do parsing stuff if index less then the length of the token
        if idx < len(token):
            # if current char is "*"
            if token[idx] == "*":
                # sets all values in range from 1 till maximum possible value
                lower_bound = 0 if controller in [60, 24] else 1
                current_res = [j for j in range(lower_bound, controller)]
                # then calls method for the next index
                current_res = self.parse_current(
                    idx + 1,
                    token,
                    current_res,
                    controller_idx,
                    controller_digits,
                    controller,
                )
            # if current char is ","
            elif token[idx] == ",":
                # check if next char is digit
                if token[idx + 1].isdigit():
                    # check if there are no other values or characters left, if no then add last number
                    if idx + len(current_number) + 1 >= len(token):
                        current_res.append(int(current_number))
                        # and increment index for current <controller> index because we already added number
                        if controller_idx + 1 < len(controller_digits):
                            controller_idx += 1
                    else:
                        # if there are chars left check if it is "/"
                        if token[idx + len(current_number) + 1] == "/":
                            # get values from range temp_minute till max possible value because upper bound is not given
                            temp_controller = current_number
                            temp_res = [
                                temp_controller
                                for temp_controller in range(
                                    int(temp_controller), controller
                                )
                            ]
                            # increment controller index if it is less then lenth of controller_digits
                            if controller_idx + 1 < len(controller_digits):
                                controller_idx += 1
                            # and parse for next char
                            current_res = self.parse_current(
                                idx + len(current_number) + 1,
                                token,
                                temp_res,
                                controller_idx,
                                controller_digits,
                                controller,
                            )
                        # if there are chars left check if it is "-"
                        elif token[idx + len(current_number) + 1] == "-":
                            # return result from next char and add to current result
                            current_res.extend(
                                self.parse_current(
                                    idx + len(current_number) + 1,
                                    token,
                                    [],
                                    controller_idx,
                                    controller_digits,
                                    controller,
                                )
                            )
                        else:
                            # if there are no chars left add last number and increment controller index
                            current_res.append(int(current_number))
                            if controller_idx + 1 < len(controller_digits):
                                controller_idx += 1

                elif token[idx + 1] == "*":
                    # return result from next "*" char and add to current result
                    current_res.extend(
                        self.parse_current(
                            idx + 1,
                            token,
                            current_res,
                            controller_idx,
                            controller_digits,
                            controller,
                        )
                    )
                else:
                    raise RuntimeError("Incorrect usage: follow argument passing rules")
                # return result from next char and add to current result
                current_res.extend(
                    self.parse_current(
                        idx + len(current_number) + 1,
                        token,
                        current_res,
                        controller_idx,
                        controller_digits,
                        controller,
                    )
                )
            elif token[idx] == "-":
                # get rangge of values
                current_res = [
                    j
                    for j in range(
                        int(controller_digits[controller_idx]),
                        int(controller_digits[controller_idx + 1]) + 1,
                    )
                ]
                # and increment contorller index
                if controller_idx + 2 < len(controller_digits):
                    controller_idx += 2
                    idx = idx + len(controller_digits[controller_idx - 1]) + 1
                else:
                    idx = idx + len(controller_digits[controller_idx + 1]) + 1
                # then parse for next char
                current_res = self.parse_current(
                    # todo
                    idx,
                    #
                    token,
                    current_res,
                    controller_idx,
                    controller_digits,
                    controller,
                )
            elif token[idx] == "/":
                # return values which are divided by current number
                current_res = [j for j in current_res if j % int(current_number) == 0]
                if controller_idx + 1 < len(controller_digits):
                    controller_idx += 1
                # parse for next char
                current_res = self.parse_current(
                    idx + len(current_number) + 1,
                    token,
                    current_res,
                    controller_idx,
                    controller_digits,
                    controller,
                )
            # check if next char is number
            elif token[idx].isdigit():
                # if next char does not exeeds lenth of token
                if idx + len(current_number) < len(token):
                    # if next char is "/" then return range to max possible value
                    if token[idx + len(current_number)] == "/":
                        temp_controller = current_number
                        current_res = [
                            temp_controller
                            for temp_controller in range(
                                int(temp_controller), controller
                            )
                        ]
                        # increment currnet index
                        if controller_idx + 1 < len(controller_digits):
                            controller_idx += 1
                        # parse for next char
                        current_res = self.parse_current(
                            idx + len(current_number),
                            token,
                            current_res,
                            controller_idx,
                            controller_digits,
                            controller,
                        )
                    # if next char is "-" parse for "-" index
                    elif token[idx + len(current_number)] == "-":
                        current_res = self.parse_current(
                            idx + len(current_number),
                            token,
                            current_res,
                            controller_idx,
                            controller_digits,
                            controller,
                        )
                    # and check if next char is ","
                    elif token[idx + len(current_number)] == ",":
                        # add number and increment controller index
                        current_res.append(int(current_number))
                        if controller_idx + 1 < len(controller_digits):
                            controller_idx += 1
                        # parse for next char
                        current_res.extend(
                            self.parse_current(
                                idx + len(current_number),
                                token,
                                [],
                                controller_idx,
                                controller_digits,
                                controller,
                            )
                        )
                # if there are chars left then add number
                else:
                    current_res.append(int(current_number))
                    if controller_idx < len(controller_digits):
                        controller_idx += 1
            return current_res
        # return from call if index exeeds the len of token
        else:
            return current_res

    # this method deletes all duplicates and sorts the lists
    def finalize(self):
        # returns dictionary with unique values from list and then casts it to list again
        self.minutes = list(dict.fromkeys(self.minutes))
        # sorts resulted list
        self.minutes.sort()

        # the same stuff here
        self.hours = list(dict.fromkeys(self.hours))
        self.hours.sort()

        self.days_month = list(dict.fromkeys(self.days_month))
        self.days_month.sort()

        self.months = list(dict.fromkeys(self.months))
        self.months.sort()

        self.days_week = list(dict.fromkeys(self.days_week))
        self.days_week.sort()
        #

    # displays results
    def dislpay(self):
        print("minute:", end=" ")
        for i in self.minutes:
            print(i, end=" ")
        print("\nhour:", end=" ")
        for i in self.hours:
            print(i, end=" ")
        print("\nday of month:", end=" ")
        for i in self.days_month:
            print(i, end=" ")
        print("\nmonth:", end=" ")
        for i in self.months:
            print(i, end=" ")
        print("\nday of week:", end=" ")
        for i in self.days_week:
            print(i, end=" ")
        print(f"\ncommand: {self.command}")

    def validate_minutes(self, minute_digits, token):
        for i in minute_digits:
            if int(i) < 0 or int(i) > 59:
                raise RuntimeError("Minute should be in range 1-60")
            self.validate_token(token)

    def validate_hours(self, hour_digits, token):
        for i in hour_digits:
            if int(i) < 0 or int(i) > 23:
                raise RuntimeError("Hour should be in range 1-24")
        self.validate_token(token)

    def validate_days_of_month(self, days_month_digits, token):
        for i in days_month_digits:
            if int(i) < 1 or int(i) > 31:
                raise RuntimeError("Day of month should be in range 1-31")
        self.validate_token(token)

    def validate_months(self, month_digits, token):
        for i in month_digits:
            if int(i) < 1 or int(i) > 12:
                raise RuntimeError("Month should be in range 1-12")
        self.validate_token(token)

    def validate_days_of_week(self, days_week_digits, token):
        for i in days_week_digits:
            if int(i) < 1 or int(i) > 7:
                raise RuntimeError("Day of week should be in range 1-7")
        self.validate_token(token)

    def validate_token(self, token):
        for i in range(len(token)):
            if token[i] not in ["/", "-", "*", ","] and not token[i].isdigit():
                raise RuntimeError("Use correct operands from [ / - * , ] and digits ")
            if token[i] == "," and i + 1 < len(token) and token[i + 1] in ["/", "-"]:
                raise RuntimeError("Use correct order of arguments")
            if (
                token[i] == "-"
                and i + 1 < len(token)
                and token[i + 1] in ["*", ",", "/"]
            ):
                raise RuntimeError("Use correct order of arguments")
            if (
                token[i] == "/"
                and i + 1 < len(token)
                and token[i + 1] in ["*", ",", "-"]
            ):
                raise RuntimeError("Use correct order of arguments")
            if token[i] == "*" and token[i + 1] in [",", "-"]:
                raise RuntimeError("Use correct order of arguments")
        if token[0] in [",", "-", "/"]:
            raise RuntimeError("Use correct order of arguments")
