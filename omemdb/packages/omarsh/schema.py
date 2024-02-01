import typing
from marshmallow.exceptions import ValidationError
from marshmallow.decorators import PRE_LOAD, POST_LOAD
from marshmallow import Schema as BaseSchema, types
from collections import OrderedDict


class Schema(BaseSchema):
    def add_field(self, key, value, last=True):
        self.declared_fields.update({key: value})
        # self.declared_fields.move_to_end(key, last=last)
        # self._update_fields(many=self.many)

    # class Meta:
    #     ordered = True

    def load(
        self,
        data: (
            typing.Mapping[str, typing.Any]
            | typing.Iterable[typing.Mapping[str, typing.Any]]
        ),
        many: bool | None = None,
        partial: bool | types.StrSequenceOrSet | None = None,
        unknown: str | None = None,
        skip_validation: bool = False,
    ):
        errors = {}
        result = OrderedDict()
        try:
            if skip_validation:
                # FIXME: seems dangerous and hard to maintain. Why not a dedicated method then?
                result = self._do_load_no_validate(data, many, partial=partial, postprocess=True)
            else:
                result = self._do_load(data, many=many, partial=partial, unknown=unknown, postprocess=True)

        except ValidationError as err:
            errors = err.messages
            valid_data = err.valid_data

        # TODO: why do we change the format? This could be problematic to change marshmallow native format
        # errors should probably rethrown and caught on higher level with a try block
        return dict(data=result, errors=errors)

    # fixme: see if we want to de-activate pre-load and post-load ?
    def _do_load_no_validate(self, data, many, partial=None, postprocess=True):
        # Callable unmarshalling object
        # unmarshal = NoValidationUnmarshaller()
        errors = {}
        many = self.many if many is None else bool(many)
        if partial is None:
            partial = self.partial
        try:
            processed_data = self._invoke_load_processors(
                PRE_LOAD,
                data,
                many,
                original_data=data)
        except ValidationError as err:
            errors = err.normalized_messages()
            result = None
        if not errors:
            try:
                result = unmarshal(
                    processed_data,
                    self.fields,
                    many=many,
                    partial=partial,
                    dict_class=self.dict_class,
                    index_errors=self.opts.index_errors,
                )
            except ValidationError as error:
                result = error.data
            # skip validation
            # self._invoke_field_validators(unmarshal, data=result, many=many)
            errors = unmarshal.errors
            # field_errors = bool(errors)
            # skip validation
            # Run schema-level migration
            # try:
            #     self._invoke_validators(unmarshal, pass_many=True, data=result, original_data=data,
            #                             many=many, field_errors=field_errors)
            # except ValidationError as err:
            #     errors.update(err.messages)
            # try:
            #     self._invoke_validators(unmarshal, pass_many=False, data=result, original_data=data,
            #                             many=many, field_errors=field_errors)
            # except ValidationError as err:
            #     errors.update(err.messages)
        # Run post processors
        if not errors and postprocess:
            try:
                result = self._invoke_load_processors(
                    POST_LOAD,
                    result,
                    many,
                    original_data=data)
            except ValidationError as err:
                errors = err.normalized_messages()
        if errors:
            # fixme: Remove self.__error_handler__ in a later release
            if self.__error_handler__ and callable(self.__error_handler__):
                self.__error_handler__(errors, data)
            exc = ValidationError(
                errors,
                field_names=unmarshal.error_field_names,
                fields=unmarshal.error_fields,
                data=data,
                **unmarshal.error_kwargs
            )
            self.handle_error(exc, data)
            if self.strict:
                raise exc

        return result, errors
