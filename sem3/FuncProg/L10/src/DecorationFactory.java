public class DecorationFactory {

    public IDecoration getDecoration(String decorationName) throws InvalidDecorationException {
        if (decorationName == null) {
            throw new InvalidDecorationException("Nazwa dekoracji nie może być pusta.");
        }

        try {
            DecorationType type = DecorationType.valueOf(decorationName.toUpperCase());

            switch (type) {
                case BAUBLES:
                    return new BaubleDecoration();
                case LIGHTS:
                    return new LightDecoration();
                case ANGEL:
                    return new AngelDecoration();
                default:
                    throw new InvalidDecorationException("Niezaimplementowany typ dekoracji: " + decorationName);
            }
        } catch (IllegalArgumentException e) {
            throw new InvalidDecorationException("Nieznana dekoracja: " + decorationName);
        }
    }
}